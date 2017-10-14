import bitstring
import socket
from fuzzywuzzy import fuzz, process
from enum import Enum
from functools import partial
import time

from .ocr_engine import engine
from . import movements
from .openstf import minicap, minitouch


class Scroll:
    def up(max_x, max_y, max_pressure):
        return movements.drag(0, max_x / 2, 0, max_x / 2, max_y,
                              max_pressure / 4, 90)

    def down(max_x, max_y, max_pressure):
        # TODO: add x and y bias, e.g 0.8 (everywhere)
        return movements.drag(0, max_x / 2, max_y * 0.8, max_x / 2, 0,
                              max_pressure / 4, 90)

    def left(max_x, max_y, max_pressure):
        return movements.drag(0, 0, max_y / 2, max_x, max_y / 2,
                              max_pressure / 4, 90)

    def right(max_x, max_y, max_pressure):
        return movements.drag(0, max_x, max_y / 2, 0, max_y / 2,
                              max_pressure / 4, 90)


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

    def _search_on_image(self, image, text):
        boxes = engine.basic_parse(image)
        best_fit = process.extractOne(
            text, [box.content for box in boxes],
            scorer=fuzz.UWRatio,
            score_cutoff=80)
        print("best_fit: ", best_fit)
        boxes = [box for box in boxes if box.content == best_fit[0]
                 ] if best_fit is not None else []
        print(boxes)
        return boxes

    def search(self, text):
        return self._search_on_image(self.get_screenshot(), text)

    def find(self, text, action, repeats=1):
        for repeat in range(0, repeats):
            boxes = self.search(text)
            if repeat + 1 == repeats:
                if not boxes:
                    raise (RuntimeError("Text '{}' not found".format(text)))
                return boxes
            if not boxes:
                action()

    def scroll_for(self, text, scroll_action=Scroll.down, repeats=1):
        _, max_x, max_y, max_pressure = self.get_minitouch_header().bounds
        movement = scroll_action(max_x, max_y, max_pressure)
        action = partial(self.perform_movement, movement)
        return self.find(text, action, repeats)

    def wait_for(self, text, timeout):
        start_time = time.time()
        while (time.time() - start_time < timeout):
            boxes = self.search(text)
            if boxes:
                break
        if not boxes:
            raise (RuntimeError("Text '{}' not found".format(text)))
        return boxes

    def tap(self, text, timeout=60, index=0):
        _, max_x, max_y, max_pressure = self.get_minitouch_header().bounds
        boxes = self.wait_for(text, timeout)
        box = boxes[index].position
        box_center = ((box.x + box.w / 2) * max_x, (box.y + box.h / 2) * max_y)
        self.perform_movement(
            movements.touch(0, *box_center, max_pressure / 4))
