# Notes
# According to the paper: "GS calculates random values using the time zones and creates a public key for AES encryption"
# So to do this, we input the current time in our timezone
# Then we get random values from the string and make a 16 byte string from it
# This could be guessed - better to use Crypto.random.get_random_bytes(16) or secrets.token_bytes(16)
# Using AES-128 - so we need a 16 byte key

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
import secrets


class Encryption:
    def __init__(self, time=None, key=None, IV=None):
        '''
        Class Constructor
        @param time: time used to generate a new cipher
        @param key: key to generate a new cipher
        @param iv: iv from an existing cipher
        '''

        if time is None:
            self._key = key
            self._IV = IV
            self._cipher = AES.new(self._key, AES.MODE_CBC, self._IV)
        else:
            self._key = self.__generate_key(time)
            self._cipher = AES.new(self._key, AES.MODE_CBC)
            self._IV = self._cipher.iv

        print(f'Encryption initialised:\n\tKey: {self._key}\n\tIV: {self._IV}')

    def __generate_key(self, time):
        '''
        Generates a 16 byte key from a datetime string
        '''
        key_string = ''.join(secrets.choice(time) for i in range(16))
        key = str.encode(key_string)
        return key

    def export_keys(self):
        '''
        Returns the key and IV used by this object's cipher
        '''
        return {
            "key": self._key,
            "IV": self._IV
        }

    def encrypt(self, data):
        '''
        Returns encrypted version of data (byte-string)
        '''
        # Convert the data to bytes if it isn't already
        if isinstance(data, bytes):
            byte_data = data
        else:
            byte_data = str.encode(data)

        return self._cipher.encrypt(pad(byte_data, AES.block_size))

    def decrypt(self, encrypted_data):
        '''
        Returns decrypted version of data (byte-string)
        '''
        cipher = AES.new(self._key, AES.MODE_CBC, iv=self._IV)
        return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()
