import shlex
import bitstring
import subprocess
import socket
import requests

from clickpecker.openstf import minicap, minitouch
from clickpecker.models.device import Device


def _get_minicap_header(minicap_address):
    with socket.socket() as sock:
        sock.connect(minicap_address)
        return minicap.read_header(sock)


def _get_minitouch_header(minitouch_address):
    with socket.socket() as sock:
        sock.connect(minitouch_address)
        return minitouch.read_header(sock)


class DeviceWrapper(object):
    def __init__(self, device, url=""):
        self.device = device
        self.url = url
        self.minicap_address = (url, self.device.minicap_port)
        self.minitouch_address = (url, self.device.minitouch_port)
        self.minicap_header = _get_minicap_header(self.minicap_address)
        self.minitouch_header = _get_minitouch_header(self.minitouch_address)

    @classmethod
    def obtain_by_device_manager(cls, device_specs, manager_url,
                                 device_url=""):
        r = requests.post(manager_url, json=device_specs)
        device = Device.from_dict(r.json()[0])
        wrapper = cls(device, device_url)
        return wrapper

    def get_screenshot(self):
        with socket.socket() as sock:
            sock.connect(self.minicap_address)
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
