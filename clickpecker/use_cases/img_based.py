from clickpecker.helpers import movements
from clickpecker.recognition import tm_engine
from clickpecker.processing import utils

def search(img, device_wrapper):
    box = tm_engine.get_match(device_wrapper.get_screenshot(), img)
    return box

def tap(img, device_wrapper):
    _, max_x, max_y, max_pressure = device_wrapper.minitouch_header.bounds
    box = search(img, device_wrapper)
    box_center = utils.get_box_center(box, max_x, max_y)
    device_wrapper.perform_movement(
        movements.touch(0, *box_center, max_pressure / 4))
