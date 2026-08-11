#!/usr/bin/env python3
"""Search a verified gain-one SPRC certificate for a balanced second-kernel promotion.

The script is self-contained and uses only the Python standard library. It verifies rooted exact
coverage before reporting a promotion. A promotion is only a diagnostic unless the resulting
kernel components can also be spliced into one path.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import struct
from collections import defaultdict
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, Iterator, Sequence, Tuple

MAGIC = b"SPRC1"
Edge = Tuple[int, Tuple[int, ...]]
Vertex = Tuple[int, ...]
Rows = Dict[Edge, int]


def canonical_cycle(xs: Sequence[int]) -> Tuple[int, ...]:
    xs = tuple(xs)
    i = xs.index(min(xs))
    return xs[i:] + xs[:i]


def transition(p: Sequence[int], k: int) -> Tuple[int, ...]:
    p = tuple(p)
    return p[k:] + tuple(reversed(p[:k]))


def endpoints(edge: Edge) -> Tuple[Vertex, ...]:
    pivot, base = edge
    return tuple(canonical_cycle(base[:i] + (pivot,) + base[i:]) for i in range(len(base)))


def doors(edge: Edge) -> Tuple[Tuple[int, ...], ...]:
    pivot, base = edge
    return tuple((pivot,) + base[i:] + base[:i] for i in range(len(base)))


def standard_kernel(n: int) -> FrozenSet[Edge]:
    pivot = n - 1
    low = tuple(range(n - 2))
    return frozenset(
        (pivot, canonical_cycle(low[:pos] + (n - 2,) + low[pos:]))
        for pos in range(n - 2)
    )


def relabel_edge(edge: Edge, perm: Sequence[int]) -> Edge:
    pivot, base = edge
    return perm[pivot], canonical_cycle(tuple(perm[x] for x in base))


def load_certificate(path: Path) -> Tuple[int, Rows]:
    data = path.read_bytes()
    if data[:5] != MAGIC:
        raise ValueError("invalid SPRC magic")
    n, base_len, count = struct.unpack("<IIQ", data[5:21])
    if base_len != n - 1:
        raise ValueError("invalid base length")
    expected = 21 + count * (2 + base_len)
    if len(data) != expected:
        raise ValueError(f"invalid file size: {len(data)} != {expected}")
    rows: Rows = {}
    offset = 21
    for _ in range(count):
        pivot = data[offset]
        parent = data[offset + 1]
        base = tuple(data[offset + 2 : offset + 2 + base_len])
        offset += 2 + base_len
        edge = (pivot, base)
        if edge in rows:
            raise ValueError("duplicate row")
        if canonical_cycle(base) != base:
            raise ValueError("noncanonical row base")
        rows[edge] = parent
    return n, rows


def validate_rooted_cover(n: int, kernel: FrozenSet[Edge], rows: Rows):
    roots = set().union(*(set(endpoints(edge)) for edge in kernel))
    child_owner: Dict[Vertex, Edge] = {}
    children: Dict[Edge, FrozenSet[Vertex]] = {}
    parents: Dict[Edge, Vertex] = {}
    for edge, parent_index in rows.items():
        eps = endpoints(edge)
        parent = eps[parent_index]
        child_set = frozenset(v for i, v in enumerate(eps) if i != parent_index)
        parents[edge] = parent
        children[edge] = child_set
        for vertex in child_set:
            if vertex in roots:
                raise ValueError("root/child overlap")
            if vertex in child_owner:
                raise ValueError("duplicate child owner")
            child_owner[vertex] = edge

    all_vertices = {canonical_cycle(p) for p in itertools.permutations(range(n))}
    if roots | set(child_owner) != all_vertices or roots & set(child_owner):
        raise ValueError("exact coverage failed")

    for edge in rows:
        seen = set()
        current = edge
        while True:
            if current in seen:
                raise ValueError("parent cycle")
            seen.add(current)
            parent = parents[current]
            if parent in roots:
                break
            if parent not in child_owner:
                raise ValueError("unrooted attachment")
            current = child_owner[parent]
    return roots, child_owner, children, parents


def relabelled_standard_packets(n: int) -> Iterator[Tuple[FrozenSet[Edge], Tuple[int, ...]]]:
    base = standard_kernel(n)
    seen = set()
    for perm in itertools.permutations(range(n)):
        packet = frozenset(relabel_edge(edge, perm) for edge in base)
        key = tuple(sorted(packet))
        if key not in seen:
            seen.add(key)
            yield packet, tuple(perm)


def all_edges(n: int) -> Iterator[Edge]:
    for pivot in range(n):
        rest = tuple(x for x in range(n) if x != pivot)
        first = min(rest)
        tail = tuple(x for x in rest if x != first)
        for suffix in itertools.permutations(tail):
            yield pivot, (first,) + suffix


def exact_covers(universe: FrozenSet[Vertex], candidates, count: int):
    by_vertex = defaultdict(list)
    for index, candidate in enumerate(candidates):
        for vertex in candidate["children"]:
            by_vertex[vertex].append(index)

    def search(remaining, chosen, used_edges):
        if not remaining:
            if len(chosen) == count:
                yield tuple(chosen)
            return
        if len(chosen) >= count or len(remaining) != 6 * (count - len(chosen)):
            return
        vertex = min(
            remaining,
            key=lambda v: sum(
                candidates[i]["children"] <= remaining
                and candidates[i]["edge"] not in used_edges
                for i in by_vertex[v]
            ),
        )
        for index in by_vertex[vertex]:
            candidate = candidates[index]
            if candidate["edge"] in used_edges or not candidate["children"] <= remaining:
                continue
            yield from search(
                remaining - candidate["children"],
                chosen + (index,),
                used_edges | {candidate["edge"]},
            )

    yield from search(universe, (), frozenset())


def validate_promotion(n, old_kernel, old_rows, packet, deleted, replacements):
    new_kernel = frozenset(set(old_kernel) | set(packet))
    new_rows = {
        edge: parent
        for edge, parent in old_rows.items()
        if edge not in packet and edge not in deleted
    }
    for edge, parent in replacements:
        if edge in new_rows or edge in new_kernel:
            return None
        new_rows[edge] = parent
    try:
        validate_rooted_cover(n, new_kernel, new_rows)
    except ValueError:
        return None
    return new_kernel, new_rows


def cut_state_path(kernel: FrozenSet[Edge], n: int, allowed_weights: Iterable[int]):
    edges = sorted(kernel)
    edge_index = {edge: i for i, edge in enumerate(edges)}
    states = []
    for edge in edges:
        for cut in doors(edge):
            states.append((edge_index[edge], edge, cut))
    starts = defaultdict(list)
    for j, (_, _, cut) in enumerate(states):
        starts[transition(cut, 2)].append(j)
    outgoing = [[] for _ in states]
    for i, (group, _, cut) in enumerate(states):
        for weight in allowed_weights:
            for j in starts.get(transition(cut, weight), ()):
                if states[j][0] != group:
                    outgoing[i].append(j)

    target_count = len(edges)
    for start in range(len(states)):
        def dfs(path, used):
            if len(used) == target_count:
                return path
            for nxt in outgoing[path[-1]]:
                group = states[nxt][0]
                if group not in used:
                    result = dfs(path + [nxt], used | {group})
                    if result is not None:
                        return result
            return None
        result = dfs([start], {states[start][0]})
        if result is not None:
            return [states[i] for i in result]
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    n, rows = load_certificate(args.certificate)
    old_kernel = standard_kernel(n)
    _, owner, children, parents = validate_rooted_cover(n, old_kernel, rows)

    oriented_rows = []
    for edge in all_edges(n):
        eps = endpoints(edge)
        for parent_index in range(n - 1):
            oriented_rows.append(
                {
                    "edge": edge,
                    "parent_index": parent_index,
                    "children": frozenset(v for i, v in enumerate(eps) if i != parent_index),
                }
            )

    selected_packets = []
    promotions = []
    packet_count = 0
    for packet, relabelling in relabelled_standard_packets(n):
        packet_count += 1
        if not packet <= rows.keys():
            continue
        selected_packets.append(packet)
        parent_vertices = frozenset(parents[edge] for edge in packet)
        deleted = frozenset(owner[v] for v in parent_vertices)
        exposed = frozenset().union(*(children[edge] for edge in deleted)) - parent_vertices
        retained = set(rows) - set(packet) - set(deleted)
        new_kernel_edges = set(old_kernel) | set(packet)
        candidates = [
            candidate
            for candidate in oriented_rows
            if candidate["children"] <= exposed
            and candidate["edge"] not in retained
            and candidate["edge"] not in new_kernel_edges
        ]
        for cover in exact_covers(exposed, candidates, len(deleted) - 1):
            replacements = [
                (candidates[i]["edge"], candidates[i]["parent_index"])
                for i in cover
            ]
            validated = validate_promotion(
                n, old_kernel, rows, packet, deleted, replacements
            )
            if validated is None:
                continue
            new_kernel, new_rows = validated
            t3_path = cut_state_path(new_kernel, n, (3,))
            any_path = cut_state_path(new_kernel, n, range(1, n + 1))
            promotions.append(
                {
                    "relabeling": list(relabelling),
                    "promoted_packet": [[e[0], list(e[1])] for e in sorted(packet)],
                    "deleted_rows": [[e[0], list(e[1])] for e in sorted(deleted)],
                    "replacement_rows": [
                        [e[0], parent, list(e[1])] for e, parent in replacements
                    ],
                    "new_kernel_rows": len(new_kernel),
                    "new_attachment_rows": len(new_rows),
                    "new_total_rows": len(new_kernel) + len(new_rows),
                    "all_weight_three_path": t3_path is not None,
                    "any_direct_cut_state_path": any_path is not None,
                }
            )
            break

    result = {
        "certificate": str(args.certificate),
        "certificate_sha256": hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
        "n": n,
        "old_kernel_rows": len(old_kernel),
        "old_attachment_rows": len(rows),
        "relabelled_standard_packets": packet_count,
        "packets_selected_as_attachments": len(selected_packets),
        "balanced_promotions": promotions,
        "new_upper_bound_claimed": False,
    }
    text = json.dumps(result, indent=2) + "\n"
    print(text, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)


if __name__ == "__main__":
    main()
