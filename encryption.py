# Notes
# According to the paper: "GS calculates random values using the time zones and creates a public key for AES encryption"
# So to do this, we input the current time in our timezone
# Then we get random values from the string and make a 16 byte string from it
# This could be guessed - better to use Crypto.random.get_random_bytes(16) or secrets.token_bytes(16)
# Using AES-128 - so we need a 16 byte key

from Crypto.Cipher import AES
from datetime import datetime
import secrets


class Encryption:
    def __init__(self, time):
        self._key = self.__generate_key(time)
        self._cipher = AES.new(self._key, AES.MODE_CBC)
        print(f'Key: {self._key }')

    def __generate_key(self, time):
        # Get 16 random characters from the time
        key_string = ''.join(secrets.choice(time) for i in range(16))
        key = str.encode(key_string)  # encode the string as bytes
        return key

    def encrypt(self, message):
        pass

    def decrypt(self, message):
        pass
