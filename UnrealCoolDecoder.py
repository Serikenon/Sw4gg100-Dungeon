import uu
import bz2
import gzip
import lzip
import lz4.frame
import lzma
import lzo # https://github.com/jd-boyd/python-lzo/issues/49
import struct
import os


ORIG_FILENAME = "amogus"


def isHex(data: str):
    return all(v in '0123456789abcdef' for v in data.lower())


def unhex(data: str):
    return bytes.fromhex(data).decode('ascii')


class VeryCoolUnpacker(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.data = open(filename, 'rb').read()

    def unpack(self) -> bytes:
        while self.__unpack():
            pass
        return self.data

    def __unpack(self) -> bool:
        if self.data.startswith(b"begin"):
            self.uuDecode()
            return True
        
        elif self.data.startswith(b'!<arch>\n'):
            self.debDecode()
            return True

        elif self.data.startswith(b'BZh'):
            self.bz2Decode()
            return True
        
        elif self.data.startswith(b'\x1f\x8b'):
            self.gzipDecode()
            return True
        
        elif self.data.startswith(b'LZIP'):
            self.lzipDecode()
            return True
    
        elif self.data.startswith(b'\x04\x22\x4D\x18'):
            self.lz4Decode()
            return True
    
        elif self.data.startswith(b'\x5d\x00\x00') or self.data.startswith(b'\xFD\x37\x7A\x58\x5A\x00'):
            self.lzmaDecode()
            return True

        elif self.data.startswith(b'\x89\x4c\x5a\x4f\x00\x0d\x0a\x1a\x0a'):
            self.lzoDecode()
            return True

        return False

    def uuDecode(self) -> None:
        print("UUDECODE Detected")
        uu.decode(self.filename, out_file='temp')
        self.data = open('temp', 'rb').read()
        os.remove('temp')
    
    def debDecode(self) -> None:
        print("DEB Detected")
        packedSize = struct.unpack("<H", self.data[0x5c:0x5e])[0]
        i = self.data.find(b'\x00\x00', 0x5e) + 2
        self.data = self.data[i:i+packedSize]

    def bz2Decode(self) -> None:
        print("BZ Detected")
        self.data = bz2.decompress(self.data)
    
    def gzipDecode(self) -> None:
        print("GZIP Detected")
        self.data = gzip.decompress(self.data)

    def lzipDecode(self) -> None:
        print("LZIP Detected")
        self.data = lzip.decompress_buffer(self.data)
    
    def lz4Decode(self) -> None:
        print("LZ4 Detected")
        self.data = lz4.frame.decompress(self.data)

    def lzmaDecode(self) -> None:
        print("LZMA Detected")
        self.data = lzma.decompress(self.data)

    def lzoDecode(self) -> None:
        print("LZO Detected")

        bufSize = int(struct.unpack('!I', self.data[0x2A:0x2E])[0])
        compressed = self.data[0x36:][:bufSize]
        header = b'\xf0' + struct.pack('!I', bufSize)

        try:
            self.data = lzo.decompress(header + compressed)
        except lzo.error:
            self.data = self.data[0x36:][:bufSize]

    
if __name__ == "__main__":
    unpacked = VeryCoolUnpacker(ORIG_FILENAME).unpack().decode().replace('\n', '')
    print("\nUnpacked:", unpacked)
    if isHex(unpacked): print("Unhexed:", unhex(unpacked))