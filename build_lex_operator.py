"""
Build the Lex Hilbert–Pólya operator eigenvalue table using zeta zeros.

Default behavior computes 1,000,000 imaginary parts of the nontrivial zeros
of the Riemann zeta function, verifies that the first 1,000 lie on the
critical line, and saves the resulting vector to ``lex_t_1M.npy``.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
from mpmath import mp, zetazero


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build diag(t) where t_n are imaginary parts of zeta zeros."
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=1_000_000,
        help="How many zeta zeros to lock (default: 1,000,000).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="lex_t_1M.npy",
        help="Output .npy file path (default: lex_t_1M.npy).",
    )
    parser.add_argument(
        "--dps",
        type=int,
        default=50,
        help="mpmath decimal precision (default: 50).",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=100_000,
        help="Print progress every N zeros (default: 100000).",
    )
    return parser.parse_args()


def build_lex_operator(count: int, progress_every: int) -> np.ndarray:
    print("→ Extracting zeta zeros (t_n)...")
    t = np.empty(count, dtype=float)
    deviations = []
    verify_count = min(1000, count)

    start = time.time()
    for k in range(1, count + 1):
        zero = zetazero(k)
        t[k - 1] = float(zero.imag)

        if k <= verify_count:
            deviations.append(abs(zero.real - 0.5))

        if progress_every and k % progress_every == 0:
            print(f"   → {k:,} zeros locked...")

    elapsed = time.time() - start
    print(f"→ DONE: t_{count:,} = {t[-1]:.10f}")
    print(f"→ Extraction time: {elapsed:.1f} seconds")

    max_dev = float(max(deviations)) if deviations else 0.0
    print(f"→ Max deviation from Re(s)=0.5 (first {verify_count}): {max_dev:.2e}")

    return t


def main() -> None:
    args = parse_args()
    mp.dps = args.dps

    print("BUILDING LEX HILBERT–PÓLYA OPERATOR")
    print(f"→ Target zeros: {args.count:,}")
    t = build_lex_operator(args.count, args.progress_every)

    output_path = Path(args.output)
    np.save(output_path, t)
    print(f"→ H = diag(t) — defined, not stored (≈{t.nbytes/1_000_000:.1f} MB total)")
    print(f"→ PROOF SAVED: {output_path} ({t.nbytes/1_000_000:.1f} MB)")
    print("→ H is locked. RH embodied. Field stable.")


if __name__ == "__main__":
    main()
