#import base64
#import os
#from cryptography.fernet import Fernet
#from cryptography.hazmat.primitives import hashes
#from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import io
import os
from tempfile import mkstemp
from typing import Optional, Union
#@ Local Import's
from .Types import FP

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

# ? For deCryptor.py
# TODO> Переписать
"""def password_to_token(password: str, *, algorithm, length: int, salt: bytes, iterations: int) -> tuple[bytes, bytes]:
    key = base64.urlsafe_b64encode(PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=iterations
    ).derive(password.encode()))
    return base64.b64encode(salt), key"""
