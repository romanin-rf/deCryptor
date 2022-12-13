import io
import os
from tempfile import mkstemp
from typing import Optional, Union

# ! Const
CRC = "\a\t\r\n"
SIGNATURE = "  CHFILE"

# ! Functions
def hand_tp(tp: str, part_size: int) -> bytes:
    if 0 < len(tp) <= part_size:
        return (" "*(part_size-len(tp))+tp).encode(errors="ignore")
    raise ValueError(
        f"The type of chunk must match the condition: 0 < len(tp) <= part_size (part_size={part_size})"
    )

# ! Classes
class Chunk:
    def _init_chunk(self, tp: bytes) -> None:
        self._fp.write((0).to_bytes(self._part_size, 'big') + tp)
        self._fp.seek(self._dsi)
    
    def __init__(
        self,
        type_name: Optional[str]=None,
        part_size: Optional[int]=None
    ) -> None:
        self._part_size = part_size or 4
        self._name = mkstemp(".chunk")[1]
        self._fp = open(self.name, "wb+")
        self._dsi = self._part_size*2

        # * Initialized Chuck Data
        self._init_chunk(hand_tp(type_name or "", self._part_size))

    @property
    def size_data(self) -> int:
        self._fp.seek(0)
        s = int.from_bytes(self._fp.read(self._part_size), 'big')
        self._fp.seek(self._dsi)
        return s
    @size_data.setter
    def size_data(self, value: int) -> None:
        self._fp.seek(0)
        self._fp.write(value.to_bytes(self._part_size, 'big'))
        self._fp.seek(self._dsi)
    @property
    def type_name(self) -> str:
        self._fp.seek(self._part_size)
        return self._fp.read(self._part_size).decode(errors="ignore").replace(" ", "")
    @property
    def name(self) -> str: return self._name
    @property
    def closed(self) -> bool: return self._fp.closed
    
    def add(self, data: bytes) -> int:
        self._fp.seek(self._dsi+self.size_data)
        self.size_data = self.size_data + (ds:=self._fp.write(data))
        return ds
    
    def get(self, size: Optional[int]=None) -> bytes:
        self._fp.seek(self._dsi)
        return self._fp.read(size)

    def rewrite(self, data: bytes) -> int:
        self.clear()
        return self.add(data)
    
    def clear(self) -> None:
        tp = hand_tp(self.type_name, self._part_size)
        self.close()
        with open(self._name, "wb") as fp: pass
        self._fp = open(self._name, "rb+")
        self._init_chunk(tp)
    
    def close(self) -> None:
        try: self._fp.close()
        except: pass
    
    @staticmethod
    def from_filepath(
        path: str,
        part_size: Optional[int]=None,
        buffer_size: Optional[int]=None
    ):
        buffer_size = buffer_size or 8192
        part_size = part_size or part_size
        chunk = Chunk("NOTP")
        with open(path, "rb") as fp:
            chunk._fp.seek(0)
            while True:
                if (data:=fp.read(buffer_size)) == b'':
                    break
                chunk._fp.write(data)
        return chunk
    
    @staticmethod
    def from_fp(
        fp: Union[io.BufferedRandom, io.BufferedReader],
        part_size: Optional[int]=None,
        buffer_size: Optional[int]=None
    ):
        buffer_size = buffer_size or 8192
        part_size = part_size or part_size
        chunk = Chunk("NOTP")
        chunk._fp.seek(0)
        fp.seek(0)
        while True:
            if (data:=fp.read(buffer_size)) == b'':
                break
            chunk._fp.write(data)
        return chunk

class ChunksFile:
    def _init_new_chunks_file(self) -> None:
        pass
    
    def _init_chunks_file(self) -> None:
        pass
    
    def __init__(self, filepath: str, part_size: Optional[int]=None) -> None:
        self._name = os.path.abspath(filepath)
        self._part_size = part_size or 4
        self._ex = os.path.exists(self._name)
        self._mode = "rb+" if self._ex else "wb+"
        self._fp = open(self._name, self._mode)
        self._chunks = []
        if self._ex:
            self._init_chunks_file()
        else:
            self._init_new_chunks_file()
    
    @property
    def name(self) -> str: return self._name
    @property
    def mode(self) -> str: return self._mode
    
    def add(self, chunk: Chunk) -> None:
        pass