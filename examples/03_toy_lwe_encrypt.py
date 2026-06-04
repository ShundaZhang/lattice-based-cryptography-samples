#!/usr/bin/env python3
"""Encrypt and decrypt bits with a tiny Regev-style LWE toy scheme."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lattice_crypto import LWEParameters, decrypt_bit, decrypt_phase, encrypt_bit, keygen


def main() -> None:
    params = LWEParameters(n=4, m=16, q=97, noise_bound=1)
    public_key, secret_key = keygen(params, seed=2026)

    print("Toy LWE parameters:", params)
    print("Secret s:", secret_key.s)
    print("Noise e: ", secret_key.e)
    print()

    bits = [0, 1, 1, 0, 1]
    for index, bit in enumerate(bits):
        ciphertext = encrypt_bit(public_key, bit, seed=100 + index)
        phase = decrypt_phase(secret_key, ciphertext)
        decoded = decrypt_bit(secret_key, ciphertext)
        print(
            f"bit={bit}  u={ciphertext.u}  v={ciphertext.v:2d}  "
            f"phase={phase:3d}  decoded={decoded}"
        )


if __name__ == "__main__":
    main()

