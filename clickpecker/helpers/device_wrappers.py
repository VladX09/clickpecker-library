import shlex
import bitstring
import subprocess
import socket
import requests
import time

from clickpecker.openstf import minicap, minitouch
from clickpecker.models.device import Device
from clickpecker.processing import image_processing
from collections import OrderedDict
from datetime import datetime
from clickpecker.configurations import default_config


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


class DeviceWrapper:
    """This class is used to interact with the test device

    Attributes:
        device: :class:`models.Device` object, containing device info
        url: Address of the host connected to the device
        minicap_address: Address of minicap server
        minitouch_address: Address of minicap server
        minicap_header: Namedtuple containing minicap protocol header
        minitouch_header: Namedtuple containing minitouch protocol header
        screen_history: Dictionary containing device's screenshot history in ``{str:PIL.Image}`` format
        screen_loging: Spicifies should device's screenshot history be saved or not
        config: Configuration dictionary containing ``device_wrapper_similarity_fun``
                and ``device_wrapper_similarity_threshold`` (see :doc:`configuration`)

    """

    def __init__(self,
                 device,
                 url="",
                 screen_loging=True,
                 config=default_config):
        self.device = device
        self.url = url
        self.minicap_address = (url, self.device.minicap_port)
        self.minitouch_address = (url, self.device.minitouch_port)
        self.minicap_header = _get_minicap_header(self.minicap_address)
        self.minitouch_header = _get_minitouch_header(self.minitouch_address)
        self.screen_history = OrderedDict()
        self.screen_logging = screen_loging
        similarity_fun = config["device_wrapper_similarity_fun"]
        similarity_threshold = config["device_wrapper_similarity_threshold"]
        # TODO: make private
        self.similarity_comparator = similarity_fun(similarity_threshold)

    def save_screenshot(self, screenshot, tag=None):
        """Save given screenshot in the history dictionary with the given tag.

        If tag is ``None``, it will be generated from current time automatically.

        Returns:
            Tag of the saved screenshot.

        """

        if tag is None:
            tag = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
        self.screen_history[tag] = screenshot
        return tag

    def load_frame(self):
        """Load current minicap frame.

        Returns:
            :class:`PIL.Image` object

        """
        with socket.socket() as sock:
            sock.connect(self.minicap_address)
            header = minicap.read_header(sock)
            frame_size = bitstring.ConstBitStream(bytes=sock.recv(4))
            frame = minicap.read_frame(sock, frame_size.uintle)
            return frame

    def save_current_screen(self, tag=None):
        """Save current screenshot in the history dictionary with the given tag.

        If tag is ``None``, it will be generated from current time automatically.

        Returns:
            Tag of the saved screenshot.

        """

        frame = self.load_frame()
        tag = self.save_screenshot(frame, tag)
        return tag

    def get_screenshot(self):
        """Get current screenshot.

        If :attr:`screen_logging` is ``True``, current screenshot will be saved to :attr:`screen_history`
        (if it differs from the last saved screenshot).
        Comparsion is configured via ``device_wrapper_similarity_fun``
        and ``device_wrapper_similarity_threshold`` (see :doc:`configuration`).

        Returns:
            :class:`PIL.Image` object

        """

        frame = self.load_frame()
        if len(self.screen_history) != 0:
            last_screenshot = list(self.screen_history.values())[-1]
            if (self.screen_logging and
                    not self.similarity_comparator(frame, last_screenshot)):
                self.save_screenshot(frame)
        else:
            self.save_screenshot(frame)
        return frame

    def perform_movement(self, movement_list):
        """Perform movement on device's screen via minitouch.

        Arguments:
            movement_list: list of strings, acceptible by `minitouch <https://github.com/openstf/minitouch>`_.
                           Common movements are listed in :mod:`helpers.movements`.

        """

        with socket.socket() as sock:
            sock.connect(self.minitouch_address)
            minitouch.send_commands(sock, movement_list)

    def adb(self, command):
        """Perform ADB command.

        Args:
            command: ADB command arguments (without `adb -s <id>`)

        Returns:
            :class:`subprocess.CompletedProcess` object

        """

        cmd = "adb -s {0} {1}".format(self.device.adb_id, command)
        return subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
