"""A compact exact-rational LLL implementation for small examples."""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

from .integer_lattice import Vector, dot, lattice_vector

FractionVector = list[Fraction]


def gram_schmidt(
    basis: Sequence[Sequence[int]],
) -> tuple[list[FractionVector], list[list[Fraction]], list[Fraction]]:
    """Return Gram-Schmidt vectors, mu coefficients, and squared norms."""

    _validate_basis(basis)
    n = len(basis)
    dimension = len(basis[0])
    b_star: list[FractionVector] = [[Fraction(0) for _ in range(dimension)] for _ in range(n)]
    mu: list[list[Fraction]] = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    norms: list[Fraction] = [Fraction(0) for _ in range(n)]

    for i in range(n):
        vector = [Fraction(x) for x in basis[i]]
        for j in range(i):
            if norms[j] == 0:
                raise ValueError("basis vectors must be linearly independent")
            mu[i][j] = _dot_fraction([Fraction(x) for x in basis[i]], b_star[j]) / norms[j]
            vector = [x - mu[i][j] * y for x, y in zip(vector, b_star[j])]
        b_star[i] = vector
        norms[i] = _dot_fraction(vector, vector)
        if norms[i] == 0:
            raise ValueError("basis vectors must be linearly independent")

    return b_star, mu, norms


def lll_reduce(
    basis: Sequence[Sequence[int]],
    *,
    delta: Fraction = Fraction(3, 4),
) -> list[Vector]:
    """Return an LLL-reduced copy of ``basis``.

    The default ``delta=3/4`` is the classical LLL value. This implementation is
    designed for clarity and small dimensions, not speed.
    """

    _validate_basis(basis)
    if not Fraction(1, 4) < delta < Fraction(1, 1):
        raise ValueError("delta must satisfy 1/4 < delta < 1")

    reduced = [list(map(int, row)) for row in basis]
    n = len(reduced)
    k = 1

    while k < n:
        _, mu, norms = gram_schmidt(reduced)

        for j in range(k - 1, -1, -1):
            q = nearest_integer(mu[k][j])
            if q != 0:
                reduced[k] = [x - q * y for x, y in zip(reduced[k], reduced[j])]
                _, mu, norms = gram_schmidt(reduced)

        lovasz_left = norms[k]
        lovasz_right = (delta - mu[k][k - 1] * mu[k][k - 1]) * norms[k - 1]
        if lovasz_left >= lovasz_right:
            k += 1
        else:
            reduced[k], reduced[k - 1] = reduced[k - 1], reduced[k]
            k = max(k - 1, 1)

    return [tuple(row) for row in reduced]


def babai_nearest_plane(
    reduced_basis: Sequence[Sequence[int]],
    target: Sequence[int],
) -> tuple[Vector, Vector]:
    """Approximate the closest lattice vector to ``target``.

    Returns ``(coefficients, lattice_vector)``. The method works best after LLL
    reduction.
    """

    _validate_basis(reduced_basis)
    if len(target) != len(reduced_basis[0]):
        raise ValueError("target dimension must match basis dimension")

    b_star, _, norms = gram_schmidt(reduced_basis)
    residual = [Fraction(x) for x in target]
    coeffs = [0] * len(reduced_basis)

    for i in range(len(reduced_basis) - 1, -1, -1):
        c = nearest_integer(_dot_fraction(residual, b_star[i]) / norms[i])
        coeffs[i] = c
        residual = [x - c * y for x, y in zip(residual, reduced_basis[i])]

    vector = lattice_vector([tuple(row) for row in reduced_basis], coeffs)
    return tuple(coeffs), vector


def nearest_integer(value: Fraction) -> int:
    """Round halves away from zero, avoiding Python's banker rounding."""

    if value >= 0:
        return int(value + Fraction(1, 2))
    return -int(-value + Fraction(1, 2))


def _dot_fraction(a: Sequence[Fraction], b: Sequence[Fraction]) -> Fraction:
    if len(a) != len(b):
        raise ValueError("dimension mismatch")
    return sum(x * y for x, y in zip(a, b))


def _validate_basis(basis: Sequence[Sequence[int]]) -> None:
    if not basis:
        raise ValueError("basis must not be empty")
    dimension = len(basis[0])
    if dimension == 0:
        raise ValueError("basis vectors must not be empty")
    for row in basis:
        if len(row) != dimension:
            raise ValueError("all basis vectors must have the same dimension")
    if len(basis) > dimension:
        raise ValueError("number of basis vectors cannot exceed ambient dimension")

