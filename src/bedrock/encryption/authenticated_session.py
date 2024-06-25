import hashlib

from Crypto.Cipher import AES
from Crypto.PublicKey import ECC

from src.bedrock.encryption.encryption_session import EncryptionSession


class AuthenticatedSession:
    """
    Provides a means for encrypting and decrypting messages.
    """

    def __init__(self, encryption_session: EncryptionSession, client_public_key: bytes):
        # convert public key to a native ECC.EccKey object to perform calculations
        self.client_public_key = ECC.import_key(client_public_key)
        self.encryption_session = encryption_session

        # compute a shared secret
        scaled_point = self.encryption_session.key.d * self.client_public_key.pointQ
        self.shared_secret = scaled_point.x.to_bytes()

        # generate a secret key
        secret_key_seed = bytearray(self.encryption_session.salt)
        secret_key_seed.extend(self.shared_secret)
        self.secret_key = hashlib.sha256(secret_key_seed).digest()

        # generate separate ciphers for encryption and decryption
        self.encrypt_cipher = AES.new(
            self.secret_key, AES.MODE_CFB, iv=self.secret_key[:16]
        )

        self.decrypt_cipher = AES.new(
            self.secret_key, AES.MODE_CFB, iv=self.secret_key[:16]
        )

    def encrypt(self, data: bytes):
        return self.encrypt_cipher.encrypt(data)

    def decrypt(self, data: bytes):
        return self.decrypt_cipher.decrypt(data)
