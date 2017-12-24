from PIL import Image

from clickpecker.use_cases import text_based, img_based
from clickpecker.helpers import movements


class BasicAPI(object):
    def __init__(self, device_wrapper, resources=None):
        self.device_wrapper = device_wrapper
        self.resources = resources

    def search(self, element, crop_x_range=(0, 1), crop_y_range=(0, 1)):
        if isinstance(element, str):
            return text_based.search(element, self.device_wrapper,
                                     crop_x_range, crop_y_range)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def find_performing_action(self, element, action, repeats, crop_x_range,
                               crop_y_range):
        if isinstance(element, str):
            return text_based.find_performing_action(
                element, action, repeats, self.device_wrapper, crop_x_range,
                crop_y_range)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def scroll_for(self,
                   element,
                   from_point_rel,
                   to_point_rel,
                   repeats=3,
                   crop_x_range=(0, 1),
                   crop_y_range=(0, 1)):
        minitouch_bounds = self.device_wrapper.minitouch_header.bounds
        movement = movements.scroll(minitouch_bounds, from_point_rel,
                                    to_point_rel)
        action = lambda: self.device_wrapper.perform_movement(movement)
        return self.find_performing_action(element, action, repeats,
                                           crop_x_range, crop_y_range)

    def adb(self, command):
        return self.device_wrapper.adb(command)

    def swipe_down(self):
        minitouch_bounds = self.device_wrapper.minitouch_header.bounds
        movement = movements.scroll(minitouch_bounds, (0.5, 0), (0.5, 1))
        self.device_wrapper.perform_movement(movement)

    def swipe_up(self):
        minitouch_bounds = self.device_wrapper.minitouch_header.bounds
        movement = movements.scroll(minitouch_bounds, (0.5, 1), (0.5, 0))
        self.device_wrapper.perform_movement(movement)

    def swipe_left(self):
        minitouch_bounds = self.device_wrapper.minitouch_header.bounds
        movement = movements.scroll(minitouch_bounds, (1, 0.5), (0, 0.5))
        self.device_wrapper.perform_movement(movement)

    def swipe_right(self):
        minitouch_bounds = self.device_wrapper.minitouch_header.bounds
        movement = movements.scroll(minitouch_bounds, (0, 0.5), (1, 0.5))
        self.device_wrapper.perform_movement(movement)

    def wait_for(self,
                 element,
                 timeout=60,
                 crop_x_range=(0, 1),
                 crop_y_range=(0, 1)):
        if isinstance(element, str):
            return text_based.wait_for(element, timeout, self.device_wrapper,
                                       crop_x_range, crop_y_range)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def tap(self,
            element,
            timeout=60,
            index=0,
            crop_x_range=(0, 1),
            crop_y_range=(0, 1)):
        if isinstance(element, str):
            text_based.tap(element, timeout, index, self.device_wrapper,
                           crop_x_range, crop_y_range)
            return
        if isinstance(element, Image.Image):
            img_based.tap(element, self.device_wrapper)
            return
        else:
            raise TypeError(
                "element must be either a string or a PIL.Image, {} is given".
                format(type(element)))
