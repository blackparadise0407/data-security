import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class AES256:
    _mode = AES.MODE_CBC
    _bs = 16

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(self._bs)
        cipher = AES.new(self.key, self._mode, iv)
        message = cipher.encrypt(raw)
        return base64.b64encode(iv + message)

    def decrypt(self, raw):
        enc = base64.b64decode(raw)
        iv = enc[: self._bs]
        cipher = AES.new(self.key, self._mode, iv)
        plain = cipher.decrypt(enc[self._bs :])
        return self._unpad(plain)

    def _pad(self, s):
        return pad(s, self._bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]
