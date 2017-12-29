import time

from clickpecker.helpers import movements
from clickpecker.recognition import ocr_engine
from clickpecker.processing import utils


def search(text, device_wrapper, config):
    return ocr_engine.search_on_image(device_wrapper.get_screenshot(), text,
                                      config)


def find_performing_action(text, action, repeats, device_wrapper, config):
    for repeat in range(0, repeats):
        boxes = search(text, device_wrapper, config)
        if repeat + 1 == repeats:
            if not boxes:
                raise (RuntimeError("Text '{}' not found".format(text)))
            return boxes
        if not boxes:
            action()


def wait_for(text, timeout, device_wrapper, config):
    start_time = time.time()
    while (time.time() - start_time < timeout):
        boxes = search(text, device_wrapper, config)
        if len(boxes) > 0:
            break
    if not boxes:
        raise (RuntimeError("Text '{}' not found".format(text)))
    return boxes


def tap(text, timeout, index, device_wrapper, config):
    _, max_x, max_y, max_pressure = device_wrapper.minitouch_header.bounds
    boxes = wait_for(text, timeout, device_wrapper, config)
    box = boxes[index].position
    box_center = utils.get_box_center(box, max_x, max_y)
    device_wrapper.perform_movement(
        movements.touch(0, *box_center, max_pressure / 4))
