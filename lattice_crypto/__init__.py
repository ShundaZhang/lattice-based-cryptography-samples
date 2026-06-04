"""Toy lattice-based cryptography helpers for learning.

The implementations in this package are intentionally small and readable.
They are not constant-time, not parameterized for real security, and must not
be used in production cryptographic systems.
"""

from .attacks import brute_force_lwe_secret, score_lwe_secret
from .integer_lattice import (
    determinant_2x2,
    dot,
    enumerate_lattice_points,
    lattice_vector,
    norm_squared,
)
from .lll import babai_nearest_plane, gram_schmidt, lll_reduce
from .lwe import (
    LWEParameters,
    LWECiphertext,
    LWEPublicKey,
    LWESecretKey,
    decrypt_bit,
    decrypt_phase,
    encrypt_bit,
    keygen,
)

__all__ = [
    "LWEParameters",
    "LWECiphertext",
    "LWEPublicKey",
    "LWESecretKey",
    "babai_nearest_plane",
    "brute_force_lwe_secret",
    "decrypt_bit",
    "decrypt_phase",
    "determinant_2x2",
    "dot",
    "encrypt_bit",
    "enumerate_lattice_points",
    "gram_schmidt",
    "keygen",
    "lattice_vector",
    "lll_reduce",
    "norm_squared",
    "score_lwe_secret",
]

