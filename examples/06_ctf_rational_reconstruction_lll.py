#!/usr/bin/env python3
"""Recover a small rational value from its residue modulo n with LLL.

Some CTF constructions accidentally reveal a value like r = A * B^{-1} mod n,
where A and B are much smaller than n. A two-dimensional lattice can recover
the small numerator and denominator.
"""

from math import gcd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lattice_crypto import lll_reduce, norm_squared


def recover_small_fraction(residue: int, modulus: int) -> tuple[int, int]:
    """Recover small coprime (numerator, denominator) from residue mod modulus."""

    reduced = lll_reduce([(residue, 1), (modulus, 0)])
    for numerator, denominator in reduced:
        if denominator == 0:
            continue
        if numerator * pow(denominator, -1, modulus) % modulus == residue:
            if gcd(numerator, denominator) == 1:
                return numerator, denominator
        if (-numerator) * pow(-denominator, -1, modulus) % modulus == residue:
            if gcd(numerator, denominator) == 1:
                return -numerator, -denominator

    raise RuntimeError("no small rational representative found")


def main() -> None:
    modulus = 1_000_000_007
    numerator = 4_243
    denominator = 1_337
    residue = numerator * pow(denominator, -1, modulus) % modulus

    print("Hidden small fraction:")
    print(f"  A / B = {numerator} / {denominator}")
    print("Public residue:")
    print(f"  r = A * B^(-1) mod n = {residue}")
    print(f"  n = {modulus}")

    basis = [(residue, 1), (modulus, 0)]
    reduced = lll_reduce(basis)
    print("\nLLL-reduced 2D basis:")
    for vector in reduced:
        print(f"  {vector}  ||v||^2={norm_squared(vector)}")

    recovered = recover_small_fraction(residue, modulus)
    print("\nRecovered small fraction:")
    print(f"  {recovered[0]} / {recovered[1]}")


if __name__ == "__main__":
    main()
