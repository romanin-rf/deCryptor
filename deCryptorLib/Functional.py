import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import io
import os
from tempfile import mkstemp
from typing import Optional, Union, List, Dict, Any
#@ Local Import's
from .Types import FP, KEY, SALT, ALGORITHM

# ? For Chunker.py
def htpn(value: Union[str, bytes], part_size: int) -> bytes:
    if isinstance(value, bytes):
        if len(value) > part_size:
            return value[:part_size]
        return (b' '*(part_size-len(value)))+value
    elif isinstance(value, str):
        if len(value) > part_size:
            return value[:part_size].encode(errors="ignore")
        return ((' '*(part_size-len(value)))+value).encode(errors="ignore")
    return (b' '*(part_size-4))+b'TYPE'

def hfp(
    fp: Optional[FP]=None,
    default_data: Optional[bytes]=None,
    buffer_size: Optional[int]=None
) -> io.BufferedRandom:
    default_data = default_data or b''
    buffer_size = buffer_size or 4096
    if isinstance(fp, str):
        fp = os.path.abspath(fp)
        if os.path.exists(fp):
            file = open(fp, 'rb+')
        else:
            path = mkstemp('.temp')[1]
            file = open(path, 'wb+')
            file.write(default_data)
            file.flush()
    elif isinstance(fp, bytes):
        path = mkstemp('.temp')[1]
        file = open(path, 'wb+')
        file.write(fp)
        file.flush()
    elif isinstance(fp, io.BytesIO):
        path = mkstemp('.temp')[1]
        file = open(path, 'wb+')
        fp.seek(0)
        while True:
            if (data:=fp.read(buffer_size)) == b'':
                break
            file.write(data)
            file.flush()
    elif isinstance(fp, io.BufferedReader):
        path = mkstemp('.temp')[1]
        file = open(path, 'wb+')
        fp.seek(0)
        while True:
            if (data:=fp.read(buffer_size)) == b'':
                break
            file.write(data)
            file.flush()
    elif isinstance(fp, io.BufferedRandom):
        file = fp
    else:
        path = mkstemp('.temp')[1]
        file = open(path, 'wb+')
        file.write(default_data)
        file.flush()
    return file

def slint(value: int, div: int) -> List[int]:
    l = []
    while value != 0:
        if value > div:
            l.append(div)
            value -= div
        else:
            l.append(value)
            value = 0
    return l

# ? For deCryptor.py
# TODO> Переписать
def text_to_token(
    text: str,
    algorithm: ALGORITHM,
    length: int,
    iterations: int
) -> tuple[SALT, KEY]:
    text: bytes = text.encode(errors="ignore")
    key = base64.urlsafe_b64encode(
        PBKDF2HMAC(
            algorithm=algorithm,
            length=length,
            salt=(salt:=base64.b64encode(text)),
            iterations=iterations
        ).derive(text)
    )
    return salt, key

def generate_key_from_password(
    password: str,
    params: Dict[str, Any]
) -> bytes: return text_to_token(password, **params)[1]