"""A tiny Regev-style LWE public-key encryption demo.

This file intentionally keeps the math visible. It omits every production
feature: secure parameters, constant-time arithmetic, CCA security transforms,
careful sampling, serialization, and side-channel defenses.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Sequence

from .integer_lattice import dot


@dataclass(frozen=True)
class LWEParameters:
    n: int = 4
    m: int = 16
    q: int = 97
    noise_bound: int = 1

    def validate(self) -> None:
        if self.n <= 0:
            raise ValueError("n must be positive")
        if self.m <= 0:
            raise ValueError("m must be positive")
        if self.q < 5:
            raise ValueError("q should be at least 5 for this toy demo")
        if self.noise_bound < 0:
            raise ValueError("noise_bound must be non-negative")


@dataclass(frozen=True)
class LWEPublicKey:
    params: LWEParameters
    A: tuple[tuple[int, ...], ...]
    b: tuple[int, ...]


@dataclass(frozen=True)
class LWESecretKey:
    params: LWEParameters
    s: tuple[int, ...]
    e: tuple[int, ...]


@dataclass(frozen=True)
class LWECiphertext:
    u: tuple[int, ...]
    v: int


def keygen(params: LWEParameters | None = None, *, seed: int | None = None) -> tuple[LWEPublicKey, LWESecretKey]:
    """Generate a tiny LWE public/secret key pair."""

    params = params or LWEParameters()
    params.validate()
    rng = random.Random(seed)

    A = tuple(tuple(rng.randrange(params.q) for _ in range(params.n)) for _ in range(params.m))
    s = tuple(rng.randrange(params.q) for _ in range(params.n))
    e = tuple(_sample_noise(params.noise_bound, rng) for _ in range(params.m))
    b = tuple((dot(row, s) + err) % params.q for row, err in zip(A, e))

    return LWEPublicKey(params=params, A=A, b=b), LWESecretKey(params=params, s=s, e=e)


def encrypt_bit(public_key: LWEPublicKey, bit: int, *, seed: int | None = None) -> LWECiphertext:
    """Encrypt one bit with the toy LWE public key."""

    if bit not in (0, 1):
        raise ValueError("bit must be 0 or 1")

    params = public_key.params
    rng = random.Random(seed)
    r = tuple(rng.randrange(2) for _ in range(params.m))
    if all(x == 0 for x in r):
        r = (1,) + r[1:]

    u = []
    for column in range(params.n):
        total = sum(r[i] * public_key.A[i][column] for i in range(params.m))
        u.append(total % params.q)

    encoded_bit = bit * (params.q // 2)
    v = (sum(r[i] * public_key.b[i] for i in range(params.m)) + encoded_bit) % params.q
    return LWECiphertext(u=tuple(u), v=v)


def decrypt_phase(secret_key: LWESecretKey, ciphertext: LWECiphertext) -> int:
    """Return centered ``v - <s,u> mod q`` before threshold decoding."""

    params = secret_key.params
    raw = (ciphertext.v - dot(secret_key.s, ciphertext.u)) % params.q
    return centered_mod(raw, params.q)


def decrypt_bit(secret_key: LWESecretKey, ciphertext: LWECiphertext) -> int:
    """Decrypt one bit by checking whether the phase is near 0 or q/2."""

    params = secret_key.params
    phase = decrypt_phase(secret_key, ciphertext)
    return 1 if abs(phase) > params.q // 4 else 0


def centered_mod(value: int, q: int) -> int:
    """Map an integer modulo q into the interval roughly (-q/2, q/2]."""

    value %= q
    if value > q // 2:
        value -= q
    return value


def _sample_noise(bound: int, rng: random.Random) -> int:
    return rng.randint(-bound, bound)


def validate_ciphertext(public_key: LWEPublicKey, ciphertext: LWECiphertext) -> None:
    """Raise ``ValueError`` if a ciphertext shape is invalid."""

    params = public_key.params
    if len(ciphertext.u) != params.n:
        raise ValueError("ciphertext.u has wrong dimension")
    if not 0 <= ciphertext.v < params.q:
        raise ValueError("ciphertext.v must be reduced modulo q")
    if any(not 0 <= x < params.q for x in ciphertext.u):
        raise ValueError("ciphertext.u entries must be reduced modulo q")

