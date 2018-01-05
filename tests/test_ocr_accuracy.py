import pytest

from . import utils
from unittest import mock
from clickpecker.use_cases import text_based, img_based
from clickpecker.recognition import ocr_engine


@pytest.mark.acc
@pytest.mark.parametrize("line",  utils.acc_lines())
@pytest.mark.parametrize("image", utils.acc_images())
def test_search_various_fonts(image, line):
    mocked_device_wrapper = mock.Mock()
    mocked_device_wrapper.get_screenshot = mock.Mock()
    mocked_device_wrapper.get_screenshot.return_value = image

    boxes = text_based.search(line, mocked_device_wrapper, (0, 1), (0, 1))
    assert len(boxes) == 1, line


@pytest.mark.verbose
@pytest.mark.parametrize("image", utils.acc_images())
def test_parse_verbose(image):
    boxes = ocr_engine.parse(image)
    print([box.content for box in boxes])
    assert 0
