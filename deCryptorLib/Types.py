import io
from typing import Union

FP = Union[
    str,
    bytes,
    io.BufferedRandom,
    io.BytesIO,
    io.BufferedReader
]