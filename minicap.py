import bitstring
import io
from PIL import Image
from select import select

def read_header(sock):
    bytelist = ["uint:8",
            "uint:8",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uint:8",
            "uint:8"]
    keys = ["version",
            "header_size",
            "pid",
            "real_width",
            "real_height",
            "virtual_width",
            "virtual_height",
            "orientation",
            "quirk"]
    header = bitstring.ConstBitStream(bytes=sock.recv(24))
    res = header.readlist(bytelist)
    res = dict(zip(keys,res))
    return(res)

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

