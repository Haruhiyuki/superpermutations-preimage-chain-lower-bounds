#!/usr/bin/env python3
"""Verify the uniform score-2(n-2) non-standard kernel family.

For target order n >= 8, the proposed kernel word is

    (n-1)^(n-3), (n-3), (n-1)^4, (n-3), (n-1)^(n-3).

The computation is in the residual permutation graph on m=n-1 symbols, exactly as in Egan's
KernelFinder. A positive digit d visits d consecutive T1 states and then applies T2 from the final
state.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence, Tuple

Perm = Tuple[int, ...]


def rotate(p: Sequence[int], k: int = 1) -> Perm:
    p = tuple(p)
    k %= len(p)
    return p[k:] + p[:k]


def transition(p: Sequence[int], k: int) -> Perm:
    p = tuple(p)
    return p[k:] + tuple(reversed(p[:k]))


def kernel_digits(n: int) -> Tuple[int, ...]:
    if n < 8:
        raise ValueError("the uniform family is stated for n >= 8")
    full = n - 1
    short = n - 3
    return (
        (full,) * (n - 3)
        + (short,)
        + (full,) * 4
        + (short,)
        + (full,) * (n - 3)
    )


def kernel_string(n: int) -> str:
    return " ".join(map(str, kernel_digits(n)))


def run_kernel(n: int):
    m = n - 1
    state: Perm = tuple(range(1, m + 1))
    visited = set()
    block_classes = []
    for block_index, d in enumerate(kernel_digits(n)):
        block = []
        q = state
        for _ in range(d):
            if q in visited:
                raise AssertionError(("repeated permutation", n, block_index, q))
            visited.add(q)
            block.append(q)
            q = rotate(q)
        canonical = min(rotate(state, k) for k in range(m))
        block_classes.append(canonical)
        state = transition(block[-1], 2)
    if len(set(block_classes)) != len(block_classes):
        raise AssertionError(("repeated cyclic class", n))
    return {
        "n": n,
        "digits": list(kernel_digits(n)),
        "kernel_string": kernel_string(n),
        "parts": len(kernel_digits(n)),
        "covered_one_cycles": len(visited),
        "score": len(visited) - (n - 2) * len(kernel_digits(n)),
        "expected_score": 2 * (n - 2),
        "distinct_block_classes": len(block_classes),
        "self_avoiding": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=8)
    parser.add_argument("--stop", type=int, default=40)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.start < 8 or args.stop < args.start:
        raise SystemExit("require 8 <= start <= stop")
    records = [run_kernel(n) for n in range(args.start, args.stop + 1)]
    for record in records:
        assert record["score"] == record["expected_score"]
    result = {
        "family": "(n-1)^(n-3) (n-3) (n-1)^4 (n-3) (n-1)^(n-3)",
        "range_checked": [args.start, args.stop],
        "all_self_avoiding": all(record["self_avoiding"] for record in records),
        "all_score_two_n_minus_two": all(
            record["score"] == 2 * (record["n"] - 2) for record in records
        ),
        "records": records,
    }
    text = json.dumps(result, indent=2) + "\n"
    print(text, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)


if __name__ == "__main__":
    main()
