#!/usr/bin/env python3
"""Brute-force a deliberately tiny LWE secret."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lattice_crypto import LWEParameters, brute_force_lwe_secret, keygen


def main() -> None:
    params = LWEParameters(n=2, m=10, q=17, noise_bound=1)
    public_key, secret_key = keygen(params, seed=7)

    print("Tiny attack parameters:", params)
    print("True secret:     ", secret_key.s)
    print("Search space:    ", params.q ** params.n, "candidates")

    recovered = brute_force_lwe_secret(public_key)
    print("Recovered secret:", recovered)
    print("Success:         ", recovered == secret_key.s)


if __name__ == "__main__":
    main()

