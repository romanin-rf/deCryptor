import io
from typing import Union, Optional
#@ Local Import's
from . import Functional as func

CHUNKS_FILE_SIGNATURE = b'CHFL\a\t\r\n'

#: Chunk
class Chunk:
    def __init__(
        self,
        fp: Union[str, bytes, io.BytesIO, io.BufferedRandom, io.BufferedReader]=None,
        part_size: Optional[int]=None
    ) -> None:
        self._ps = part_size or 4
        self._fp: io.BufferedRandom = func.hfp(fp, (b'\x00'*self._ps)+func.htpn(b'CHNK', self._ps))
        self._si, self._ti, self._di = 0, self._ps, self._ps*2

    @property
    def name(self) -> str: return self._fp.name
    
    @property
    def part_size(self) -> str: return self._ps
    
    @property
    def size_data(self) -> int:
        self._fp.seek(self._si)
        return int.from_bytes(self._fp.read(self._ps), 'big')
    
    @size_data.setter
    def size_data(self, value: int) -> None:
        self._fp.seek(self._si)
        self._fp.write(value.to_bytes(self._ps, 'big'))
        self._fp.flush()
    
    @property
    def type_name(self) -> bytes:
        self._fp.seek(self._ti)
        return self._fp.read(self._ps)
    
    @type_name.setter
    def type_name(self, value: Union[str, bytes]) -> None:
        self._fp.seek(self._ti)
        self._fp.write(func.htpn(value, self._ps))
        self._fp.flush()
    
    @property
    def closed(self) -> bool: return self._fp.closed
    
    def seek(self, index: int) -> int:
        if index >= 0:
            return self._fp.seek(index+self._di)-self._di
        raise ValueError("The index cannot be less than 0")
    
    def read(self, size: Optional[int]=None) -> bytes:
        if self._fp.tell() < self._di:
            self._fp.seek(self._di)
        return self._fp.read(size)
    
    def write(self, data: bytes) -> int:
        if self._fp.tell() < self._di:
            self._fp.seek(self._di)
        s = self._fp.write(data)
        self._fp.flush()
        return s
    
    def add(self, data: bytes) -> int:
        sd = self.size_data
        self._fp.seek(self._di+sd)
        self.size_data = sd + (s:=self._fp.write(data))
        self._fp.flush()
        return s
    
    def clear(self) -> None:
        if not self._fp.closed:
            tn, sz = self.type_name, self.size_data
            self._fp.close()
            self._fp = func.hfp(None, sz.to_bytes(self._ps, 'big')+tn)
        else:
            self._fp = func.hfp(None, (b'\x00'*self._ps)+func.htpn(b'CHNK', self._ps))
    
    def rewrite(self, data: bytes) -> int:
        self.clear()
        return self.add(data)

#: ChunksFile Class
class ChunksFile:
    def __init__(
        self,
        fp: Union[str, bytes, io.BytesIO, io.BufferedRandom, io.BufferedReader]=None
    ) -> None:
        self._fp = func.hfp(fp, CHUNKS_FILE_SIGNATURE)
        self._chunks = []
    
    @property
    def name(self) -> str: return self._fp.name
