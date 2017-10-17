import bitstring
import socket
from fuzzywuzzy import fuzz, process
from functools import partial
import time
import subprocess

from . import movements
from . import tm_engine
from .ocr_engine import engine
from .openstf import minicap, minitouch


class Scroll:
    def up(max_x, max_y, max_pressure):
        return movements.drag(0, max_x / 2, max_y * 0.2, max_x / 2,
                              max_y * 0.8, max_pressure / 4, 90)

    def down(max_x, max_y, max_pressure):
        return movements.drag(0, max_x / 2, max_y * 0.8, max_x / 2,
                              max_y * 0.2, max_pressure / 4, 90)

    def left(max_x, max_y, max_pressure):
        return movements.drag(0, 0, max_y / 2, max_x, max_y / 2,
                              max_pressure / 4, 90)

    def right(max_x, max_y, max_pressure):
        return movements.drag(0, max_x, max_y / 2, 0, max_y / 2,
                              max_pressure / 4, 90)


class Device:
    def __init__(self, minicap_address, minitouch_address, adb_id):
        self.adb_id = adb_id
        self.minicap_address = minicap_address
        self.minitouch_address = minitouch_address
        self.minitouch_header = self.get_minitouch_header()
        self.minicap_header = self.get_minicap_header()

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
            return minicap.read_frame(sock, frame_size.uintle)

    def perform_movement(self, movement_list):
        with socket.socket() as sock:
            sock.connect(self.minitouch_address)
            minitouch.send_commands(sock, movement_list)

    def search(self, text, x_range=(0,1), y_range=(0,1)):
        return engine.search_on_image(self.get_screenshot(), text, x_range,
                                     y_range)

    def find(self, text, action, repeats=1, x_range=(0,1), y_range=(0,1)):
        for repeat in range(0, repeats):
            boxes = self.search(text, x_range, y_range)
            if repeat + 1 == repeats:
                if not boxes:
                    raise (RuntimeError("Text '{}' not found".format(text)))
                return boxes
            if not boxes:
                action()

    def scroll_for(self,
                   text,
                   scroll_action=Scroll.down,
                   repeats=1,
                   x_range=(0,1),
                   y_range=(0,1)):
        _, max_x, max_y, max_pressure = self.minitouch_header.bounds
        movement = scroll_action(max_x, max_y, max_pressure)
        action = partial(self.perform_movement, movement)
        return self.find(text, action, repeats, x_range, y_range)

    def wait_for(self, text, timeout, x_range=(0,1), y_range=(0,1)):
        start_time = time.time()
        while (time.time() - start_time < timeout):
            boxes = self.search(text, x_range, y_range)
            if boxes:
                break
        if not boxes:
            raise (RuntimeError("Text '{}' not found".format(text)))
        return boxes

    def _get_box_center(self, box, max_x, max_y):
        return ((box.x + box.w / 2) * max_x, (box.y + box.h / 2) * max_y)

    def tap(self, text, timeout=60, index=0, x_range=(0,1), y_range=(0,1)):
        _, max_x, max_y, max_pressure = self.minitouch_header.bounds
        boxes = self.wait_for(text, timeout, x_range, y_range)
        box = boxes[index].position
        box_center = self._get_box_center(box, max_x, max_y)
        self.perform_movement(
            movements.touch(0, *box_center, max_pressure / 4))

    def tap_img(self, img):
        _, max_x, max_y, max_pressure = self.minitouch_header.bounds
        box = tm_engine.get_match(self.get_screenshot(), img)
        box_center = self._get_box_center(box, max_x, max_y)
        self.perform_movement(
            movements.touch(0, *box_center, max_pressure / 4))

    def adb(self, command):
        command = "adb -s {0} {1}".format(self.adb_id, command)
        return subprocess.run(command.split(" "), stdout=subprocess.PIPE)
