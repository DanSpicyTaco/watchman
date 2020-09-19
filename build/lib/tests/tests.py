import unittest
from datetime import datetime
from lib import encryption


class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.string = "A random string we use for testing!"
    # self.encryptor =

    def test_encryption_and_decryption(self):
        current_time = datetime.now().isoformat()
        encryptor = encryption.Encryption(time=current_time)
        encrypted_data = encryptor.encrypt(self.string)
        decrypted_data = encryptor.decrypt(encrypted_data)
        self.assertEqual(decrypted_data, self.string)

    def test_export_keys(self):
        current_time = datetime.now().isoformat()
        encryptor = encryption.Encryption(time=current_time)
        encrypted_data = encryptor.encrypt(self.string)

        keys = encryptor.export_keys()
        encryptor2 = encryption.Encryption(key=keys["key"], IV=keys["IV"])

        decrypted_data = encryptor2.decrypt(encrypted_data)
        self.assertEqual(decrypted_data, self.string)
