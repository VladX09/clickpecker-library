from PIL import Image

import contextlib
from clickpecker.use_cases import text_based, img_based
from clickpecker.helpers import movements


class BasicAPI(object):
    """Basic API class which is used to perform actions on the testing device.

    Attributes:
        device_wrapper: :class:`clickpecker.helpers.DeviceWrapper` object
        default_config: Dictonary with all necessary variables (see :doc:`configuration`)

    """
    def __init__(self, device_wrapper, default_config, resources=None):
        # TODO: remove resources
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
        """Search given string on device's screen.

        Args:
            element: Search text
            config:  Custom config

        Returns:
            List of boxes containing search text (or similar enough)

        Raises:
            TypeError: if **element** is not ``str``

        """

        config = self.merge_config(config)

        if isinstance(element, str):
            return text_based.search(element, self.device_wrapper, config)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def find_performing_action(self, element, action, repeats, config=None):
        """Repeat given action till text is found.

        Args:
            element: Search text
            action:  Function to perform
            repeats: Number of attempts
            config:  Custom config

        Returns:
            List of boxes containing search text (or similar enough)

        Raises:
            TypeError: if **element** is not ``str``
            RuntimeError: if **element** was not found

        """

        config = self.merge_config(config)

        if isinstance(element, str):
            return text_based.find_performing_action(
                element, action, repeats, self.device_wrapper, config)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def scroll_for(self, element, from_point_rel, to_point_rel, config=None):
        """Scroll device's screen in given direction till text is found.

        Maximum number of scrolls can be customized via ``config["api_scroll_repeats"]``

        Args:
            element: Search text
            from_point_rel: Scroll start relative point
            to_point_rel: Scroll end relative point
            config:  Custom config

        Returns:
            List of boxes containing search text (or similar enough)

        Raises:
            TypeError: if **element** is not ``str``
            RuntimeError: if **element** was not found

        """

        config = self.merge_config(config)
        repeats = config["api_scroll_repeats"]

        minitouch_bounds = self.device_wrapper.minitouch_header.bounds
        movement = movements.scroll(minitouch_bounds, from_point_rel,
                                    to_point_rel)
        action = lambda: self.device_wrapper.perform_movement(movement)
        return self.find_performing_action(element, action, repeats, config)

    def adb(self, command):
        """Perform ADB command.

        Args:
            command: ADB command arguments (without `adb -s <id>`)

        Returns:
            :class:`subprocess.CompletedProcess` object

        """

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
        """Wait for text appears.

        Repeatively search given text on the screen untill time is out.
        Timeout can be customized via ``config["api_wait_timeout"]``

        Args:
            element: Search text
            config:  Custom config

        Returns:
            List of boxes containing search text (or similar enough)

        Raises:
            TypeError: if **element** is not ``str``
            RuntimeError: if **element** was not found

        """

        config = self.merge_config(config)
        timeout = config["api_wait_timeout"]

        if isinstance(element, str):
            return text_based.wait_for(element, timeout, self.device_wrapper,
                                       config)
        else:
            raise TypeError(
                "element must be a string, {} is given".format(type(element)))

    def tap(self, element, config=None):
        """Tap given element(text or image).

        Waiting timeout before tap can be customized via ``config["api_tap_timeout"]``.
        If several occurances were found, needed one can be chosen via
        ``config["api_tap_index"]``

        Args:
            element: Search text
            config:  Custom config

        Raises:
            TypeError: if **element** is not ``str`` or ``PIL.Image``
            RuntimeError: if **element** was not found

        """

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

    def save_current_screen(self, tag=None):
        """Save current screenshot in the history dictionary with the given tag.

        If tag is ``None``, it will be generated from current time automatically.

        Returns:
            Tag of saved screenshot.

        """

        return self.device_wrapper.save_current_screen(tag)

    def screen_similar_with(self, tag, config=None):
        """Check if current screenshot is similar with the screenshot having the given tag.

        Similarity function can be customized via ``config["api_similarity_fun"]``
        (see functions in :mod:`processing.image_processing`).
        Similarity threshold can be customized via ``config["api_similarity_threshold"]``

        Returns:
            ``True`` if screenshots are similar with given accurcy

        """

        config = self.merge_config(config)

        similarity_fun= config["api_similarity_fun"]
        similarity_threshold = config["api_similarity_threshold"]
        similarity_comparator = similarity_fun(similarity_threshold)

        current_screen = self.device_wrapper.get_screenshot()
        saved_screen = self.device_wrapper.screen_history[tag]
        return similarity_comparator(current_screen, saved_screen)

    @contextlib.contextmanager
    def assert_screen_change(self, config=None):
        """Assert that device screen will change after follow operations.

        Uses :meth:`screen_similar_with` for comparsion

        Raises:
            AssertionError

        """

        config = self.merge_config(config)

        # Save current screenshot with unique tag
        tag = self.device_wrapper.save_current_screen()
        # Perform any testing process
        yield
        # Raise error if screen was not changed
        assert not self.screen_similar_with(tag, config), "Screen wasn't changed"

    @contextlib.contextmanager
    def assert_screen_same(self, config=None):
        """Assert that device screen will not change after follow operations.

        Uses :meth:`screen_similar_with` for comparsion

        Raises:
            AssertionError

        """

        config = self.merge_config(config)

        # Save current screenshot with unique tag
        tag = self.device_wrapper.save_current_screen()
        # Perform any testing process
        yield
        # Raise error if screen was changed
        assert self.screen_similar_with(tag, config), "Screen was changed"
