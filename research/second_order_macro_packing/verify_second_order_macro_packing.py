#!/usr/bin/env python3
"""
Global second-order macro-packing audit for the superpermutation lower-bound program.

This program does not claim a new arbitrary-k lower bound. It verifies three pieces of
evidence for a general support-aware, higher-order method:

1. Generalized low-defect macro spectrum.
   For 2 <= delta <= f <= k-4, construct an explicit exact-W3 block
   B_{k,delta,f}, verify its parameters, and check that among the six exact-W3
   same-type successor orientations there is exactly one support-disjoint successor.

2. Neutral bridge macro orbits.
   For the bridge type (delta,f)=(2,k-4), verify the explicit Theta orbit,
   its period lambda_k, cumulative support-disjointness, and collision on return.

3. Integer macro-support packing.
   Enumerate every relabelled complete bridge macro for k=7,8 and compute the
   exact maximum number of pairwise support-disjoint macro supports. For k=9,
   construct a deterministic fixed-marker packing of size at least 24.

All computations use exact integer/tuple arithmetic and the Python standard library.
"""
from __future__ import annotations
import itertools
import json
import math
import random
from pathlib import Path
from typing import Any


def req(value: bool, message: object) -> None:
    if not value:
        raise AssertionError(message)


def rot(word: tuple[int, ...], amount: int = 1) -> tuple[int, ...]:
    amount %= len(word)
    return word[amount:] + word[:amount]


def canon(word: tuple[int, ...]) -> tuple[int, ...]:
    return rot(word, word.index(0))


def overlap_weight(source: tuple[int, ...], target: tuple[int, ...]) -> int:
    n = len(source)
    for dropped in range(1, n + 1):
        if source[dropped:] == target[: n - dropped]:
            return dropped
    raise AssertionError("empty overlap must work")


def piece_support(start: tuple[int, ...], size: int) -> frozenset[tuple[int, ...]]:
    marker = start[-1]
    base = start[:-1]
    return frozenset(canon((marker,) + rot(base, i)) for i in range(size))


def piece_end(start: tuple[int, ...], size: int) -> tuple[int, ...]:
    return (start[-1],) + rot(start[:-1], size - 1)


def w3_starts(head: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    output = tuple(head[3:] + tail for tail in itertools.permutations(head[:3]))
    req(all(overlap_weight(head, start) == 3 for start in output), "W3 generation")
    return output


def relword(word: tuple[int, ...], labeling: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(labeling[x] for x in word)


def relsupport(
    support: frozenset[tuple[int, ...]],
    labeling: tuple[int, ...],
) -> frozenset[tuple[int, ...]]:
    return frozenset(canon(relword(word, labeling)) for word in support)


def generalized_block(k: int, delta: int, full_count: int) -> dict[str, Any]:
    """
    Explicit generalized bridge block B_{k,delta,f}.

    Put n=k-1, marker m=n, c=n-delta-1, and
        O=(c+2,...,n-1,0,...,c-1,c+1).
    The first piece has size n-delta and the following f pieces are full.
    """
    n = k - 1
    marker = n
    c = n - delta - 1
    req(2 <= delta <= full_count <= k - 4, (k, delta, full_count))

    orbit = tuple(range(c + 2, n)) + tuple(range(c)) + (c + 1,)
    req(len(orbit) == n - 1, "orbit length")
    starts = [(tuple(range(k)), n - delta)]
    starts.extend((rot(orbit, j) + (c, marker), n) for j in range(full_count))

    for left, right in zip(starts, starts[1:]):
        req(overlap_weight(piece_end(*left), right[0]) == 3, "not exact W3")

    supports = [piece_support(*piece) for piece in starts]
    union = frozenset().union(*supports)
    req(sum(map(len, supports)) == len(union), "block self-intersection")

    head = piece_end(*starts[-1])
    theta = rot(orbit, full_count) + (c, marker)
    req(theta in w3_starts(head), "theta is not an exact-W3 successor")

    classes = n * (full_count + 1) - delta
    defect = (n - 1) * delta - (full_count + 1)
    req(len(union) == classes, ("class count", k, delta, full_count))

    intersections = []
    zero_starts = []
    for start in w3_starts(head):
        target_support = relsupport(union, start)
        intersection = len(union & target_support)
        intersections.append(intersection)
        if intersection == 0:
            zero_starts.append(start)

    return {
        "k": k,
        "n": n,
        "delta": delta,
        "full_count": full_count,
        "piece_count": full_count + 1,
        "classes": classes,
        "defect": defect,
        "defect_density": defect / classes,
        "head": head,
        "theta": theta,
        "candidate_intersections": intersections,
        "zero_starts": zero_starts,
        "support": union,
    }


def permutation_order(permutation: tuple[int, ...]) -> tuple[int, list[list[int]]]:
    seen: set[int] = set()
    order = 1
    cycles: list[list[int]] = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycle = []
        x = start
        while x not in seen:
            seen.add(x)
            cycle.append(x)
            x = permutation[x]
        cycles.append(cycle)
        order = math.lcm(order, len(cycle))
    return order, cycles


def bridge_lambda(k: int) -> int:
    n = k - 1
    if n % 3 == 0:
        return 2 * (n // 3)
    if n % 3 == 1:
        m = (n - 1) // 3
        return m * (2 * m + 1)
    m = (n - 2) // 3
    return (m + 1) * (2 * m + 1)


def compose_labeling(
    current: tuple[int, ...],
    transition: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(current[i] for i in transition)


def bridge_macro_support(k: int) -> tuple[frozenset[tuple[int, ...]], dict[str, Any]]:
    block = generalized_block(k, 2, k - 4)
    theta = tuple(block["theta"])
    order, cycles = permutation_order(theta)
    req(order == bridge_lambda(k), ("bridge period", k, order))

    current = tuple(range(k))
    used: frozenset[tuple[int, ...]] = frozenset()
    for step in range(order):
        support = relsupport(block["support"], current)
        req(not (support & used), ("early bridge collision", k, step))
        used |= support
        current = compose_labeling(current, theta)

    req(current == tuple(range(k)), ("bridge orbit did not close", k))
    repeat = relsupport(block["support"], current)
    req(bool(repeat & used), ("bridge return did not collide", k))
    return used, {
        "k": k,
        "block_classes": block["classes"],
        "block_defect": block["defect"],
        "lambda": order,
        "theta_cycles": cycles,
        "macro_classes": len(used),
        "macro_defect": order * block["defect"],
    }


def rotation_universe(k: int) -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], int]]:
    universe = [(0,) + tail for tail in itertools.permutations(range(1, k))]
    return universe, {word: i for i, word in enumerate(universe)}


def support_bitset(
    support: frozenset[tuple[int, ...]],
    labeling: tuple[int, ...],
    index: dict[tuple[int, ...], int],
) -> int:
    bits = 0
    for word in support:
        bits |= 1 << index[canon(relword(word, labeling))]
    return bits


def all_labelled_macro_supports(k: int) -> tuple[int, list[int], dict[int, tuple[int, ...]], dict[str, Any]]:
    support, macro = bridge_macro_support(k)
    universe, index = rotation_universe(k)
    unique: dict[int, tuple[int, ...]] = {}
    for labeling in itertools.permutations(range(k)):
        bits = support_bitset(support, labeling, index)
        unique.setdefault(bits, labeling)
    sets = list(unique)
    return len(universe), sets, unique, macro


def disjointness_graph(sets: list[int]) -> tuple[list[int], int]:
    n = len(sets)
    adjacency = [0] * n
    edges = 0
    for i, left in enumerate(sets):
        for j in range(i + 1, n):
            if not (left & sets[j]):
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
                edges += 1
    return adjacency, edges


def exact_max_clique(adjacency: list[int]) -> tuple[list[int], int]:
    """Exact bitset branch-and-bound with a greedy coloring upper bound."""
    best: list[int] = []
    nodes = 0

    def color_sort(candidates: int) -> tuple[list[int], list[int]]:
        vertices: list[int] = []
        bounds: list[int] = []
        color = 0
        remaining = candidates
        while remaining:
            color += 1
            available = remaining
            while available:
                least = available & -available
                vertex = least.bit_length() - 1
                vertices.append(vertex)
                bounds.append(color)
                remaining &= ~least
                available &= ~least
                available &= ~adjacency[vertex]
        return vertices, bounds

    def expand(clique: list[int], candidates: int) -> None:
        nonlocal best, nodes
        nodes += 1
        if not candidates:
            if len(clique) > len(best):
                best = clique.copy()
            return
        vertices, bounds = color_sort(candidates)
        for i in range(len(vertices) - 1, -1, -1):
            if len(clique) + bounds[i] <= len(best):
                return
            vertex = vertices[i]
            if not ((candidates >> vertex) & 1):
                continue
            expand(clique + [vertex], candidates & adjacency[vertex])
            candidates &= ~(1 << vertex)

    expand([], (1 << len(adjacency)) - 1)
    return best, nodes


def exact_bridge_packing(k: int) -> dict[str, Any]:
    universe_size, sets, labels, macro = all_labelled_macro_supports(k)
    adjacency, edges = disjointness_graph(sets)
    clique, nodes = exact_max_clique(adjacency)
    macro_size = sets[0].bit_count()
    selected = [labels[sets[i]] for i in clique]
    return {
        **macro,
        "rotation_classes": universe_size,
        "distinct_labelled_macro_supports": len(sets),
        "disjointness_edges": edges,
        "disjointness_degree": 2 * edges // len(sets),
        "trivial_capacity": universe_size // macro_size,
        "exact_max_packing": len(clique),
        "covered_classes": len(clique) * macro_size,
        "uncovered_classes": universe_size - len(clique) * macro_size,
        "covered_fraction": len(clique) * macro_size / universe_size,
        "branch_and_bound_nodes": nodes,
        "packing_labels": selected,
    }


def fixed_marker_k9_packing() -> dict[str, Any]:
    k = 9
    support, macro = bridge_macro_support(k)
    universe, index = rotation_universe(k)
    expected = math.factorial(k - 1) // macro["lambda"]
    unique: dict[int, tuple[int, ...]] = {}

    for prefix in itertools.permutations(range(1, k)):
        labeling = prefix + (0,)
        bits = support_bitset(support, labeling, index)
        unique.setdefault(bits, labeling)
        if len(unique) == expected:
            break
    req(len(unique) == expected, "failed to enumerate fixed-marker translate orbit")

    sets = list(unique)
    adjacency, edges = disjointness_graph(sets)
    rng = random.Random(20260811)
    best: list[int] = []
    for _ in range(5000):
        candidates = (1 << len(sets)) - 1
        clique: list[int] = []
        while candidates:
            count = candidates.bit_count()
            sample: list[int] = []
            if count <= 180:
                work = candidates
                while work:
                    least = work & -work
                    sample.append(least.bit_length() - 1)
                    work &= ~least
            else:
                seen: set[int] = set()
                while len(sample) < 80:
                    vertex = rng.randrange(len(sets))
                    if ((candidates >> vertex) & 1) and vertex not in seen:
                        sample.append(vertex)
                        seen.add(vertex)
            vertex = max(
                sample,
                key=lambda v: (adjacency[v] & candidates).bit_count() + rng.random(),
            )
            clique.append(vertex)
            candidates &= adjacency[vertex]
        if len(clique) > len(best):
            best = clique
        if len(best) >= 24:
            break

    req(len(best) >= 24, ("k=9 packing regression", len(best)))
    macro_size = sets[0].bit_count()
    return {
        **macro,
        "rotation_classes": len(universe),
        "fixed_marker_macro_supports": len(sets),
        "fixed_marker_disjointness_edges": edges,
        "trivial_capacity": len(universe) // macro_size,
        "certified_packing_lower_bound": len(best),
        "covered_classes": len(best) * macro_size,
        "uncovered_classes": len(universe) - len(best) * macro_size,
        "packing_labels": [unique[sets[i]] for i in best],
        "exact_upper_bound_status": "not proved",
    }


def main(output: Path) -> dict[str, Any]:
    generalized_rows = []
    for k in range(6, 25):
        for delta in range(2, k - 3):
            for full_count in range(delta, k - 3):
                row = generalized_block(k, delta, full_count)
                req(row["zero_starts"] == [row["theta"]], (
                    "generalized macro successor",
                    k,
                    delta,
                    full_count,
                    row["candidate_intersections"],
                ))
                generalized_rows.append({
                    key: value
                    for key, value in row.items()
                    if key not in {"support", "zero_starts"}
                })

    bridge_rows = []
    for k in range(7, 25):
        _, row = bridge_macro_support(k)
        bridge_rows.append(row)

    exact_rows = [exact_bridge_packing(7), exact_bridge_packing(8)]
    k9 = fixed_marker_k9_packing()

    result = {
        "status": "PASS",
        "scope": {
            "generalized_macro_statement_checked": "2 <= delta <= f <= k-4",
            "generalized_macro_k_range": [6, 24],
            "generalized_macro_instances": len(generalized_rows),
            "bridge_orbit_k_range": [7, 24],
            "exact_all-label_packing_k": [7, 8],
            "constructive_fixed-marker_packing_k": [9],
        },
        "generalized_macro_spectrum": generalized_rows,
        "bridge_macro_orbits": bridge_rows,
        "exact_bridge_macro_packings": exact_rows,
        "k9_bridge_macro_packing": k9,
        "interpretation": {
            "first_order_barrier": (
                "single-component affine charging cannot see the integrality loss "
                "between labelled macro supports"
            ),
            "second_order_object": (
                "pairwise-disjoint left translates of a macro support in S_{k-1}"
            ),
            "arbitrary_k_status": (
                "the support-packing reduction is exact; the generalized successor "
                "formula is finite-audited here and still requires a traditional arbitrary-k proof"
            ),
        },
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    report = main(here / "second_order_macro_packing_report.json")
    print(json.dumps({
        "status": report["status"],
        "generalized_instances": report["scope"]["generalized_macro_instances"],
        "k7_exact": report["exact_bridge_macro_packings"][0]["exact_max_packing"],
        "k8_exact": report["exact_bridge_macro_packings"][1]["exact_max_packing"],
        "k9_constructed": report["k9_bridge_macro_packing"]["certified_packing_lower_bound"],
    }, indent=2))
