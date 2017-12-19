import bitstring
import io

from PIL import Image
from select import select
from collections import namedtuple

MinicapKeys = [
    "version", "header_size", "pid", "real_width", "real_height",
    "virtual_width", "virtual_height", "orientation", "quirk"
]

MinicapHeader = namedtuple("MinicapHeader", MinicapKeys)


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
        "uint:8"
    ]
    version = read_version(sock)
    if (version != 1):
        raise RuntimeError("Unsuppoted minicap version: {}".format(version))
    header = bitstring.ConstBitStream(bytes=sock.recv(23))
    header = header.readlist(bytelist)
    header = [version] + header
    header = MinicapHeader(**dict(zip(MinicapKeys, header)))
    return (header)


def read_frame(sock, framesize):
    data = b''
    sock.setblocking(False)
    while True:
        if len(data) >= framesize:
            break
        rd, _, _ = select([sock], [], [], 0)
        if sock in rd:
            msg = sock.recv(framesize - len(data))
            data += msg
    sock.setblocking(True)
    return Image.open(io.BytesIO(data))
