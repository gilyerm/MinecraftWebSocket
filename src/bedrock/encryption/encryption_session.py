from base64 import b64encode

from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes


class EncryptionSession:
    def __init__(self):
        self.key = ECC.generate(curve="P-384")
        self.salt = get_random_bytes(16)
        self.public_key = self.key.public_key().export_key(format="DER")

        # convenience attrs,
        # passed into the authentication payload
        self.b64_public_key = b64encode(self.public_key).decode()
        self.b64_salt = b64encode(self.salt).decode()
