"""Tiny attacks that explain parameter growth.

These helpers are deliberately inefficient and only work for very small toy
parameters. They are here to build intuition, not to attack real schemes.
"""

from __future__ import annotations

from itertools import product
from typing import Sequence

from .integer_lattice import dot
from .lwe import LWEPublicKey, centered_mod


def score_lwe_secret(public_key: LWEPublicKey, secret_guess: Sequence[int]) -> int:
    """Return the largest absolute residual for a guessed LWE secret."""

    params = public_key.params
    if len(secret_guess) != params.n:
        raise ValueError("secret guess has wrong dimension")

    residuals = [
        abs(centered_mod(b_i - dot(row, secret_guess), params.q))
        for row, b_i in zip(public_key.A, public_key.b)
    ]
    return max(residuals)


def brute_force_lwe_secret(
    public_key: LWEPublicKey,
    *,
    max_candidates: int = 2_000_000,
) -> tuple[int, ...]:
    """Recover a tiny LWE secret by exhaustive search.

    A candidate is accepted when every public-key residual is within the known
    toy noise bound. Real LWE parameters make this search astronomically large.
    """

    params = public_key.params
    candidate_count = params.q ** params.n
    if candidate_count > max_candidates:
        raise ValueError(
            f"refusing to enumerate {candidate_count} candidates; "
            f"raise max_candidates only for tiny teaching parameters"
        )

    for guess in product(range(params.q), repeat=params.n):
        if score_lwe_secret(public_key, guess) <= params.noise_bound:
            return tuple(guess)

    raise ValueError("no secret matched the public samples")

