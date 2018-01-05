import shlex
import bitstring
import subprocess
import socket
import requests
import time

from clickpecker.openstf import minicap, minitouch
from clickpecker.models.device import Device
from clickpecker.processing import image_processing


def _reconnect_on_error(func, address, timeout):
    start_time = time.time()
    while (time.time() - start_time < timeout):
        with socket.socket() as sock:
            sock.connect(address)
            try:
                result = func(sock)
                return result
            except ConnectionError as e:
                sock.close()
    raise ConnectionError("No header received")


def _get_minicap_header(minicap_address):
    header = _reconnect_on_error(minicap.read_header, minicap_address, 60)
    return header


def _get_minitouch_header(minitouch_address, timeout=60):
    header = _reconnect_on_error(minitouch.read_header, minitouch_address, 60)
    return header


class DeviceWrapper(object):
    def __init__(self,
                 device,
                 url="",
                 screen_loging=True,
                 similarity_fun=image_processing.check_ssim_similar(
                     treshold=0.9, multichannel=True)):
        self.device = device
        self.url = url
        self.minicap_address = (url, self.device.minicap_port)
        self.minitouch_address = (url, self.device.minitouch_port)
        self.minicap_header = _get_minicap_header(self.minicap_address)
        self.minitouch_header = _get_minitouch_header(self.minitouch_address)
        self.screen_history = []
        self.screen_logging = screen_loging
        self.similarity_fun = similarity_fun

    def get_screenshot(self):
        with socket.socket() as sock:
            sock.connect(self.minicap_address)
            header = minicap.read_header(sock)
            frame_size = bitstring.ConstBitStream(bytes=sock.recv(4))
            frame = minicap.read_frame(sock, frame_size.uintle)

            # Save screen history log
            if (self.screen_logging and
                (len(self.screen_history) == 0
                 or not self.similarity_fun(frame, self.screen_history[-1]))):
                self.screen_history.append(frame)
            return frame

    def perform_movement(self, movement_list):
        with socket.socket() as sock:
            sock.connect(self.minitouch_address)
            minitouch.send_commands(sock, movement_list)

    def adb(self, command):
        cmd = "adb -s {0} {1}".format(self.device.adb_id, command)
        return subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
