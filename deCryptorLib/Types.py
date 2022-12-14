import io
from cryptography.hazmat.primitives import hashes
from typing import Union

FP = Union[
    str,
    bytes,
    io.BufferedRandom,
    io.BytesIO,
    io.BufferedReader
]
KEY = bytes
SALT = bytes
ALGORITHM = hashes.SHA256