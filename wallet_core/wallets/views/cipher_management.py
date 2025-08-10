
import os
import base64
from web3 import Web3, Account
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from django.conf import settings


class CipherUtility:
    def __init__(self):
        self.password = settings.SECRET_KEY.encode("utf-8")
        self.backend = default_backend()
        self.block_size = 128  # AES block size in bits

    def encrypt_private_key(self, private_key: bytes):
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._derive_key(salt)

        # Pad private key to block size
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(private_key) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "salt": base64.b64encode(salt).decode(),
            "iv": base64.b64encode(iv).decode()
        }

    def decrypt_private_key(self, encrypted_data: dict):
        salt = base64.b64decode(encrypted_data["salt"])
        iv = base64.b64decode(encrypted_data["iv"])
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])
        key = self._derive_key(salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(self.block_size).unpadder()
        private_key = unpadder.update(padded) + unpadder.finalize()

        return private_key

    def _derive_key(self, salt):
        return PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit AES key
            salt=salt,
            iterations=100000,
            backend=self.backend
        ).derive(self.password)

