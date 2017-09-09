import bitstring
import socket
import io
import binascii
from PIL import Image
from PIL import ImageFile
from select import select

def parse_header(header):
    header = bitstring.ConstBitStream(bytes=header)
    list = ["uint:8",
            "uint:8",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uintle:32",
            "uint:8",
            "uint:8"]
    res = header.readlist(list)
    keys = ["version",
            "header_size",
            "pid",
            "real_width",
            "real_height",
            "virtual_width",
            "virtual_height",
            "orientation",
            "quirk"]
    res = dict(zip(keys,res))
    return(res)

def read_header(address):
    with socket.socket() as sock:
        sock.connect(address)
        header = sock.recv(24)
        return parse_header(header)

def parse_frame(frame):
    return Image.open(io.BytesIO(frame))

def _save_image(img):
    filename = input("filename [test.jpg]: ")
    img.save(filename if len(filename) > 0 else "test.jpg")

def _save_image(img, filename):
    img.save(filename)

def recvimage(sock):
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
    return(data)

def read_frame(address):
    with socket.socket() as sock:
        sock.connect(address)
        header = parse_header(sock.recv(24))
        print("header: ", header)
        frame_size = bitstring.ConstBitStream(bytes=sock.recv(4))
        data = recvimage(sock)
        return parse_frame(data)

if __name__ == "__main__":
    address = ("",1313)
    img = read_frame(address)
    _save_image(img, "test.jpg")
    print("done")
