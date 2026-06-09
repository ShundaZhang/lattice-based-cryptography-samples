#!/usr/bin/env python3
"""Solve a tiny CTF-style subset-sum instance with LLL.

This mirrors the lattice embedding often used against weak knapsack
cryptosystems in CTFs. Real challenges use larger dimensions and Sage/fpylll;
this toy instance is intentionally small enough for the educational LLL in this
repository.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lattice_crypto import lll_reduce


def subset_sum_lattice(weights: list[int], target: int) -> list[tuple[int, ...]]:
    """Build the classic subset-sum embedding matrix."""

    dimension = len(weights) + 1
    basis: list[list[int]] = []

    for i, weight in enumerate(weights):
        row = [0] * dimension
        row[i] = 1
        row[-1] = weight
        basis.append(row)

    final_row = [0] * dimension
    final_row[-1] = -target
    basis.append(final_row)
    return [tuple(row) for row in basis]


def recover_bits(weights: list[int], target: int) -> tuple[int, ...]:
    """Recover 0/1 subset bits by searching the LLL-reduced basis."""

    reduced = lll_reduce(subset_sum_lattice(weights, target))
    for vector in reduced:
        bits = vector[:-1]
        if vector[-1] == 0 and all(bit in (0, 1) for bit in bits):
            if sum(weight * bit for weight, bit in zip(weights, bits)) == target:
                return bits

        negated_bits = tuple(-bit for bit in bits)
        if vector[-1] == 0 and all(bit in (0, 1) for bit in negated_bits):
            if sum(weight * bit for weight, bit in zip(weights, negated_bits)) == target:
                return negated_bits

    raise RuntimeError("LLL did not reveal the subset; try a lower-density instance")


def bits_to_text(bits: tuple[int, ...]) -> str:
    """Decode bits as ASCII bytes."""

    chars = []
    for offset in range(0, len(bits), 8):
        byte = bits[offset : offset + 8]
        chars.append(chr(int("".join(map(str, byte)), 2)))
    return "".join(chars)


def main() -> None:
    message = "OK"
    bits = tuple(int(bit) for byte in message.encode() for bit in f"{byte:08b}")

    # A low-density toy public key. The weights are intentionally large and
    # random-looking so the wanted bit vector is unusually short in the lattice.
    weights = [
        424633559245,
        978312965548,
        44856014165,
        534871852898,
        913999456057,
        392988992260,
        981858150271,
        240223516435,
        152591468918,
        151634339699,
        106425369465,
        878929203004,
        588122882666,
        777415144757,
        665004820126,
        162888563211,
    ]
    target = sum(weight * bit for weight, bit in zip(weights, bits))

    recovered = recover_bits(weights, target)

    print("Weights:")
    print(" ", weights)
    print("Target:")
    print(" ", target)
    print("Recovered bits:")
    print(" ", "".join(map(str, recovered)))
    print("Decoded message:")
    print(" ", bits_to_text(recovered))


if __name__ == "__main__":
    main()
