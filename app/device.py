import bitstring
import socket
import openstf.minicap
import openstf.minitouch

class Device:

    def __init__(self, minicap_address, minitouch_address):
        self.minicap_address = minicap_address
        self.minitouch_address = minitouch_address

    def get_minicap_header(self):
        with socket.socket() as sock:
            sock.connect(self.minicap_address)
            return minicap.read_header(sock)

    def get_minitouch_header(self):
        with socket.socket() as sock:
            sock.connect(self.minitouch_address)
            return minitouch.read_header(sock)

    def get_screenshot(self):
        with socket.socket() as sock:
            sock.connect(self.minicap_address)
            header = minicap.read_header(sock)
            frame_size = bitstring.ConstBitStream(bytes=sock.recv(4))
            return minicap.read_frame(sock)

    def perform_movement(self, movement_list):
        with socket.socket() as sock:
            sock.connect(self.minitouch_address)
            minitouch.send_commands(sock, movement_list)

def _save_image(img):
    filename = input("filename [test.jpg]: ")
    img.save(filename if len(filename) > 0 else "test.jpg")

def _save_image(img, filename):
    img.save(filename)
