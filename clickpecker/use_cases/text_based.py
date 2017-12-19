import time

from clickpecker.helpers import movements
from clickpecker.recognition import ocr_engine
from clickpecker.processing import utils


def search(text, device_wrapper, crop_x_range, crop_y_range):
    return ocr_engine.search_on_image(device_wrapper.get_screenshot(), text,
                                      crop_x_range, crop_y_range)


def find_performing_action(text, action, repeats, device_wrapper, crop_x_range,
                           crop_y_range):
    for repeat in range(0, repeats):
        boxes = search(text, device_wrapper, crop_x_range, crop_y_range)
        if repeat + 1 == repeats:
            if not boxes:
                raise (RuntimeError("Text '{}' not found".format(text)))
            return boxes
        if not boxes:
            action()


def wait_for(text, timeout, device_wrapper, crop_x_range, crop_y_range):
    start_time = time.time()
    while (time.time() - start_time < timeout):
        boxes = search(text, device_wrapper, crop_x_range, crop_y_range)
        if boxes:
            break
    if not boxes:
        raise (RuntimeError("Text '{}' not found".format(text)))
    return boxes


def tap(text, timeout, index, device_wrapper, crop_x_range, crop_y_range):
    _, max_x, max_y, max_pressure = device_wrapper.minitouch_header.bounds
    boxes = wait_for(text, timeout, device_wrapper, crop_x_range, crop_y_range)
    box = boxes[index].position
    box_center = utils.get_box_center(box, max_x, max_y)
    device_wrapper.perform_movement(
        movements.touch(0, *box_center, max_pressure / 4))
