import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings


def generate_key():
    password = settings.SECRET_KEY.encode()
    salt = f'{os.urandom(16)}'.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))

    return key


def encrypt_value(value):
    key = generate_key()
    f = Fernet(key)
    value_hash = f.encrypt(value.encode())
    encrypted_value = f'{key.decode()}^{value_hash.decode()}'

    return encrypted_value


def decrypt_value(value):
    key, value_hash = value.split('^')
    f = Fernet(key.encode())
    decrypted_value = f.decrypt(value_hash.encode())

    return decrypted_value
