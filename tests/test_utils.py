from django.test import TestCase
from v1.utils.base_utils import card_mask, make_hash, encrypt, decrypt, short_fullname, phone_mask


class UtilsTests(TestCase):

    def test_card_mask(self):
        self.assertEqual(card_mask("8600123412341234"), "860012xxxxxx1234")

    def test_phone_mask(self):
        self.assertEqual(phone_mask("+99891 234 56 78"), "+9989x xxx xx xx")

    def test_short_fullname(self):
        self.assertEqual(short_fullname("Muzaffar Makhkamov"), "Makhkamov M.")

    def test_hash_consistency(self):
        h1 = make_hash("testdata")
        h2 = make_hash("testdata")
        self.assertEqual(h1, h2)

    def test_hash_with_secret(self):
        h1 = make_hash("data", "secret123")
        h2 = make_hash("data", "secret123")
        self.assertEqual(h1, h2)

    def test_encryption_and_decryption(self):
        key = "mytestkey123"
        original = "8600123412341234"
        encrypted = encrypt(original, key)
        decrypted = decrypt(encrypted, key)
        self.assertEqual(original, decrypted)
