import io
import os
from typing import Union, Optional, Dict
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
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._fp.name}', part_size={self._ps}, type_name={self.type_name}, size_data={self.size_data}, closed={self._fp.closed})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __del__(self) -> None:
        self.close()

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
    
    def close(self) -> None:
        if not self._fp.closed:
            self._fp.close()
    
    def clear(self) -> None:
        n = self._fp.name
        if not self._fp.closed:
            tn, sz = self.type_name, self.size_data
            self._fp.close()
            try: os.remove(n)
            except: pass
            self._fp = func.hfp(n, sz.to_bytes(self._ps, 'big')+tn)
        else:
            try: os.remove(n)
            except: pass
            self._fp = func.hfp(n, (b'\x00'*self._ps)+func.htpn(b'CHNK', self._ps))
    
    def rewrite(self, data: bytes) -> int:
        self.clear()
        return self.add(data)

#: ChunksFile Class
class ChunksFile:
    def _init_chunks(self) -> None:
        self._fp.seek(0)
        cfs = self._fp.read(len(CHUNKS_FILE_SIGNATURE))
        if cfs != CHUNKS_FILE_SIGNATURE:
            raise TypeError('The data is not ChunksFile data')
        while True:
            if (data:=self._fp.read(self._ps*2)) == b'':
                break
            chunk = Chunk(self._ps)
            size = int.from_bytes(data[:self._ps], 'big')
            type_name = data[self._ps:]
            chunk.type_name = type_name
            for i in func.slint(size, self._bs):
                chunk.add(self._fp.read(i))
            self._chunks[type_name] = chunk
    
    def __init__(
        self,
        fp: Union[str, bytes, io.BytesIO, io.BufferedRandom, io.BufferedReader]=None,
        part_size: Optional[int]=None,
        buffer_size: Optional[int]=None
    ) -> None:
        self._fp = func.hfp(fp, CHUNKS_FILE_SIGNATURE)
        self._ps = part_size or 4
        self._bs = buffer_size or 4096
        self._chunks: Dict[str, Chunk] = {}
        self._init_chunks()

    def __str__(self) -> str: return f"{self.__class__.__name__}(name='{self._fp.name}', {self._chunks})"
    def __repr__(self) -> str: return self.__str__()
    def __del__(self) -> None: self.close()
    def __getitem__(self, key: str) -> Chunk:
        return self._chunks[key]
    def __setitem__(self, key: str, value: Chunk) -> None:
        assert isinstance(value, Chunk)
        self._chunks[key] = value
    def __delitem__(self, key: str) -> None:
        del self._chunks[key]
    
    @property
    def name(self) -> str: return self._fp.name
    @property
    def closed(self) -> str: return self._fp.closed

    def add(self, chunk: Chunk) -> None:
        if isinstance(chunk, Chunk):
            self._chunks[chunk.type_name] = chunk
    
    def delete(self, type_name: Chunk) -> Optional[Chunk]:
        return self._chunks.pop(type_name, None)
    
    def clear(self) -> None:
        n = self._fp.name
        if not self._fp.closed:
            self._fp.close()
        try: os.remove(n)
        except: pass
        self._fp = func.hfp(n, CHUNKS_FILE_SIGNATURE)
    
    def flush(self) -> None:
        self.clear()
        self._fp.seek(len(CHUNKS_FILE_SIGNATURE))
        for i in self._chunks:
            if not self._chunks[i]._fp.closed:
                self._chunks[i]._fp.seek(0)
                while True:
                    if (data:=self._chunks[i]._fp.read(self._bs)) == b'':
                        break
                    self._fp.write(data)
                    self._fp.flush()
    
    def save(self, filepath: str) -> None:
        self.flush()
        with open(filepath, 'wb') as file:
            self._fp.seek(0)
            while True:
                if (data:=self._fp.read(self._bs)) == b'':
                    break
                file.write(data)
                file.flush()
    
    def close(self) -> None:
        if not self._fp.closed:
            self.flush()
            self._fp.close()
