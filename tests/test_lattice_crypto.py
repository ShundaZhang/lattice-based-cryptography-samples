import unittest

from lattice_crypto import (
    LWEParameters,
    brute_force_lwe_secret,
    decrypt_bit,
    determinant_2x2,
    encrypt_bit,
    enumerate_lattice_points,
    keygen,
    lll_reduce,
    norm_squared,
)


class LatticeBasicsTest(unittest.TestCase):
    def test_determinant_and_enumeration(self) -> None:
        basis = [(4, 1), (1, 3)]
        self.assertEqual(determinant_2x2(basis), 11)

        vectors = [vector for _, vector in enumerate_lattice_points(basis, 1, include_zero=False)]
        self.assertIn((1, 3), vectors)
        self.assertIn((-1, -3), vectors)

    def test_lll_reduces_first_vector_norm(self) -> None:
        basis = [(105, 821, 404), (17, 137, 71), (48, 365, 192)]
        reduced = lll_reduce(basis)
        self.assertLessEqual(norm_squared(reduced[0]), norm_squared(basis[0]))


class LWETest(unittest.TestCase):
    def test_encrypt_decrypt_bits(self) -> None:
        params = LWEParameters(n=4, m=16, q=97, noise_bound=1)
        public_key, secret_key = keygen(params, seed=2026)

        for index, bit in enumerate([0, 1, 1, 0, 1]):
            ciphertext = encrypt_bit(public_key, bit, seed=100 + index)
            self.assertEqual(decrypt_bit(secret_key, ciphertext), bit)

    def test_tiny_bruteforce_attack(self) -> None:
        params = LWEParameters(n=2, m=10, q=17, noise_bound=1)
        public_key, secret_key = keygen(params, seed=7)

        recovered = brute_force_lwe_secret(public_key)
        self.assertEqual(recovered, secret_key.s)


if __name__ == "__main__":
    unittest.main()

