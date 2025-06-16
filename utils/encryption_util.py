import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class EncryptionUtil:
    """Utility for AES encryption/decryption using CBC mode with PKCS7 padding."""

    def __init__(self):
        key_b64 = os.getenv("ENCRYPTION_KEY")
        iv_b64 = os.getenv("ENCRYPTION_IV")
        if not key_b64 or not iv_b64:
            raise ValueError("ENCRYPTION_KEY or ENCRYPTION_IV not set")

        self.key = base64.b64decode(key_b64)
        self.iv = base64.b64decode(iv_b64)
        if len(self.iv) != 16:
            raise ValueError("IV must be 16 bytes for AES CBC")
        if len(self.key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes for AES")

        self._cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))

    def encrypt(self, data: bytes) -> bytes:
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded = padder.update(data) + padder.finalize()
        encryptor = self._cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return base64.b64encode(ciphertext)

    def decrypt(self, token: bytes) -> bytes:
        decryptor = self._cipher.decryptor()
        padded = decryptor.update(base64.b64decode(token)) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded) + unpadder.finalize()
        return data
