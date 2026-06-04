"""Small integer-lattice utilities.

Basis vectors are represented as rows:

    basis = [(b11, b12, ...), (b21, b22, ...), ...]

A lattice vector is an integer linear combination of those row vectors.
"""

from __future__ import annotations

from itertools import product
from typing import Iterable, Iterator, Sequence

Vector = tuple[int, ...]
Basis = Sequence[Vector]


def dot(a: Sequence[int], b: Sequence[int]) -> int:
    """Return the integer dot product of two vectors."""

    _check_same_dimension(a, b)
    return sum(x * y for x, y in zip(a, b))


def norm_squared(v: Sequence[int]) -> int:
    """Return the squared Euclidean norm."""

    return dot(v, v)


def add(a: Sequence[int], b: Sequence[int]) -> Vector:
    """Return vector addition."""

    _check_same_dimension(a, b)
    return tuple(x + y for x, y in zip(a, b))


def scale(c: int, v: Sequence[int]) -> Vector:
    """Return scalar-vector multiplication."""

    return tuple(c * x for x in v)


def lattice_vector(basis: Basis, coeffs: Sequence[int]) -> Vector:
    """Return sum_i coeffs[i] * basis[i]."""

    if len(basis) != len(coeffs):
        raise ValueError("number of coefficients must match number of basis vectors")
    if not basis:
        return ()

    dimension = len(basis[0])
    out = [0] * dimension
    for coeff, row in zip(coeffs, basis):
        if len(row) != dimension:
            raise ValueError("all basis vectors must have the same dimension")
        for j, value in enumerate(row):
            out[j] += coeff * value
    return tuple(out)


def determinant_2x2(basis: Sequence[Sequence[int]]) -> int:
    """Return the determinant of a 2D row-basis matrix."""

    if len(basis) != 2 or len(basis[0]) != 2 or len(basis[1]) != 2:
        raise ValueError("determinant_2x2 expects two 2D basis vectors")
    (a, b), (c, d) = basis
    return a * d - b * c


def enumerate_lattice_points(
    basis: Basis,
    coeff_bound: int,
    *,
    include_zero: bool = True,
) -> Iterator[tuple[Vector, Vector]]:
    """Yield ``(coeffs, vector)`` for coeffs in [-coeff_bound, coeff_bound].

    This is exponential in the number of basis vectors. It is useful for
    two-dimensional and tiny teaching examples only.
    """

    if coeff_bound < 0:
        raise ValueError("coeff_bound must be non-negative")

    ranges: Iterable[range] = (range(-coeff_bound, coeff_bound + 1) for _ in basis)
    for coeffs in product(*ranges):
        vector = lattice_vector(basis, coeffs)
        if not include_zero and all(x == 0 for x in vector):
            continue
        yield tuple(coeffs), vector


def _check_same_dimension(a: Sequence[int], b: Sequence[int]) -> None:
    if len(a) != len(b):
        raise ValueError(f"dimension mismatch: {len(a)} != {len(b)}")

