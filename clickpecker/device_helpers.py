import shlex
import bitstring
import subprocess
import socket

from clickpecker.openstf import minicap, minitouch
from clickpecker import movements

MinitouchBounds = namedtuple(
    "MinitouchBounds", ["max_contacts", "max_x", "max_y", "max_pressure"])
MinitouchHeader = namedtuple("MinitouchHeader", ["version", "bounds", "pid"])
MinicapHeader = namedtuple("MinicapHeader", minicap.MinicapKeys)


def _get_minicap_header(url, minicap_port):
    with socket.socket() as sock:
        sock.connect(url, minicap_port)
        return minicap.read_header(sock)


def _get_minitouch_header(url, minitouch_port):
    with socket.socket() as sock:
        sock.connect(url, minitouch_port)
        return minitouch.read_header(sock)


class DeviceHelper(object):
    def __init__(self, device, url=""):
        self.device = device
        self.device_url = url
        self.minicap_header = _get_minicap_header(url, device.minicap_port)
        self.minitouch_header = _get_minitouch_header(url,
                                                      device.minitouch_port)

    def get_screenshot(self):
        with socket.socket() as sock:
            sock.connect(self.url, self.device.minicap_port)
            header = minicap.read_header(sock)
            frame_size = bitstring.ConstBitStream(bytes=sock.recv(4))
            return minicap.read_frame(sock, frame_size.uintle)

    def perform_movement(self, movement_list):
        with socket.socket() as sock:
            sock.connect(self.minitouch_address)
            minitouch.send_commands(sock, movement_list)

    def adb(self, command):
        cmd = "adb -s {0} {1}".format(self.device.adb_id, command)
        return subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
