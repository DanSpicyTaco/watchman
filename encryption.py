# https://www.pycryptodome.org/en/latest/src/cipher/classic.html
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Encryption:
    def __init__(self, time_info):
        # TODO Calculate key using time information
        self._time_info = time_info
        self._key = get_random_bytes(16)
        print(self._key)

        # cipher = AES.new(key, AES.MODE_CBC)

    # def
