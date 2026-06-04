#!/usr/bin/env python3
"""Enumerate a tiny 2D lattice and inspect short vectors."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lattice_crypto import determinant_2x2, enumerate_lattice_points, norm_squared


def main() -> None:
    basis = [(4, 1), (1, 3)]
    print("Basis:", basis)
    print("det(L):", abs(determinant_2x2(basis)))

    points = list(enumerate_lattice_points(basis, coeff_bound=2, include_zero=False))
    shortest = sorted(points, key=lambda item: norm_squared(item[1]))[:8]

    print("\nShortest non-zero vectors with coeffs in [-2,2]:")
    for coeffs, vector in shortest:
        print(f"  coeffs={str(coeffs):>8}  vector={str(vector):>8}  ||v||^2={norm_squared(vector)}")


if __name__ == "__main__":
    main()
