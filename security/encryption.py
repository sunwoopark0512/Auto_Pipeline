import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class EncryptionUtil:
    """Utility for AES-256/CBC encryption/decryption."""

    def __init__(self, key: bytes):
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes for AES-256")
        self.key = key

    @staticmethod
    def load_key() -> bytes:
        """Load key from DATA_ENCRYPT_KEY env var, generate if absent."""
        key_b64 = os.getenv("DATA_ENCRYPT_KEY")
        if key_b64:
            try:
                return base64.b64decode(key_b64)
            except Exception:
                pass
        key = os.urandom(32)
        os.environ["DATA_ENCRYPT_KEY"] = base64.b64encode(key).decode()
        return key

    @classmethod
    def from_env(cls) -> "EncryptionUtil":
        return cls(cls.load_key())

    def encrypt(self, data: bytes) -> bytes:
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded) + encryptor.finalize()
        return base64.b64encode(iv + encrypted)

    def decrypt(self, token: bytes) -> bytes:
        raw = base64.b64decode(token)
        iv, ciphertext = raw[:16], raw[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded) + unpadder.finalize()
