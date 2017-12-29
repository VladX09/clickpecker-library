from PIL import Image

from clickpecker.use_cases import text_based, img_based
from clickpecker.helpers import movements


class BasicAPI(object):
    def __init__(self, device_wrapper, default_config, resources=None):
        self.device_wrapper = device_wrapper
        self.default_config = default_config
        self.resources = resources

    def merge_config(self, custom_config):
        config = dict(self.default_config)
        if custom_config is not None:
            for k, v in custom_config.items():
                config[k] = v
        return config

    def search(self, element, config=None):

        config = self.merge_config(config)

        if isinstance(element, str):
            return text_based.search(element, self.device_wrapper, config)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def find_performing_action(self, element, action, repeats, config=None):

        config = self.merge_config(config)

        if isinstance(element, str):
            return text_based.find_performing_action(
                element, action, repeats, self.device_wrapper, config)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def scroll_for(self, element, from_point_rel, to_point_rel, config=None):

        config = self.merge_config(config)
        repeats = config["api_scroll_repeats"]

        minitouch_bounds = self.device_wrapper.minitouch_header.bounds
        movement = movements.scroll(minitouch_bounds, from_point_rel,
                                    to_point_rel)
        action = lambda: self.device_wrapper.perform_movement(movement)
        return self.find_performing_action(element, action, repeats, config)

    def adb(self, command):
        return self.device_wrapper.adb(command)

    # TODO: add argument for X and Y fixed position
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

    def wait_for(self, element, config=None):

        config = self.merge_config(config)
        timeout = config["api_wait_timeout"]

        if isinstance(element, str):
            return text_based.wait_for(element, timeout, self.device_wrapper,
                                       config)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def tap(self, element, config=None):

        config = self.merge_config(config)
        timeout = config["api_tap_timeout"]
        index = config["api_tap_index"]

        if isinstance(element, str):
            text_based.tap(element, timeout, index, self.device_wrapper,
                           config)
            return
        if isinstance(element, Image.Image):
            img_based.tap(element, self.device_wrapper, config)
            return
        else:
            raise TypeError(
                "element must be either a string or a PIL.Image, {} is given".
                format(type(element)))
