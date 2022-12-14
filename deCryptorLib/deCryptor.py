
#@ Import typing
from typing import Optional
#@ Fernet importing
from cryptography.fernet import Fernet
#@ Local Import's
from .Types import ALGORITHM
from .Functional import generate_key_from_password


class deCryptor:
    def __init__(
        self,
        algorithm: Optional[ALGORITHM]=None,
        length: Optional[int]=None,
        iterations: Optional[int]=None
    ) -> None:
        self.g_kwargs = {"algorithm": algorithm, "length": length, "iterations": iterations}
    
    def key_from_text(self, text: bytes) -> bytes:
        return generate_key_from_password(text, self.g_kwargs)
    
    def fernet_from_text(self, text: bytes) -> Fernet:
        return Fernet(self.key_from_text(text))
    
    def encode(self, data: bytes, key: bytes) -> bytes:
        pass