import bitstring
import io
from PIL import Image
from select import select
from ..datatypes import MinicapHeader

def read_version(sock):
    return bitstring.ConstBitStream(bytes=sock.recv(1)).uint

def read_header(sock):
    bytelist = [
            # "uint:8",
            "uint:8",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uint:8",
            "uint:8"]
    version = read_version(sock)
    if(version != 1):
        raise RuntimeError("Unsuppoted minicap version: {}".format(version))
    header = bitstring.ConstBitStream(bytes=sock.recv(23))
    header = header.readlist(bytelist)
    header = [version] + header
    header = MinicapHeader(**dict(zip(KEYS, header)))
    return(header)

def read_frame(sock):
    data = b''
    sock.setblocking(False)
    while True:
        rd,_,_ = select([sock],[],[],0)
        if sock in rd:
            msg = sock.recv(2)
            data += msg
            if msg == b'' or msg  == bytes.fromhex('ff d9'):
                break
        else:
            break
    sock.setblocking(True)
    return Image.open(io.BytesIO(data))
