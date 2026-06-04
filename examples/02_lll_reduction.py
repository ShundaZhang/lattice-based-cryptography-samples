#!/usr/bin/env python3
"""Run LLL and Babai nearest plane on a small integer lattice."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lattice_crypto import babai_nearest_plane, lll_reduce, norm_squared


def print_basis(label: str, basis: list[tuple[int, ...]]) -> None:
    print(label)
    for row in basis:
        print(f"  {row!s:>18}  ||b||^2={norm_squared(row)}")


def main() -> None:
    basis = [(105, 821, 404), (17, 137, 71), (48, 365, 192)]
    reduced = lll_reduce(basis)

    print_basis("Original basis:", basis)
    print()
    print_basis("LLL-reduced basis:", reduced)

    target = (50, 400, 200)
    coeffs, near = babai_nearest_plane(reduced, target)
    error = tuple(t - v for t, v in zip(target, near))
    print("\nBabai nearest-plane demo:")
    print("  target:       ", target)
    print("  coefficients: ", coeffs)
    print("  lattice point:", near)
    print("  error:        ", error, "||error||^2=", norm_squared(error))


if __name__ == "__main__":
    main()

