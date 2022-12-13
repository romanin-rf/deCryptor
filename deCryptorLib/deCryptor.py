import os
import datetime
import uuid
import base64
# * Import typing
from typing import Union
# * Fernet importing
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class deCryptor:
    def __init__(self) -> None:
        pass
    
    