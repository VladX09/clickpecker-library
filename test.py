import bitstring
import socket
from openstf import minicap

class Device:

    def __init__(self, minicap_address):
        self.minicap_address = minicap_address

    def get_header(self):
        with socket.socket() as sock:
            sock.connect(self.minicap_address)
            return minicap.read_header(sock)

    def get_frame(self):
        with socket.socket() as sock:
            sock.connect(self.minicap_address)
            header = minicap.read_header(sock)
            frame_size = bitstring.ConstBitStream(bytes=sock.recv(4))
            return minicap.read_frame(sock)

def _save_image(img):
    filename = input("filename [test.jpg]: ")
    img.save(filename if len(filename) > 0 else "test.jpg")

def _save_image(img, filename):
    img.save(filename)

if __name__ == "__main__":
    address = ("",1313)
    dev = Device(address)
    img = dev.get_frame()
    _save_image(img, "test.jpg")
    print("done")
