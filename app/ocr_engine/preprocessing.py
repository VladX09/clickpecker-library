import PIL
import cv2
import numpy as np
from ..namedtuples import Box
from . import utils

def binary(pil_image, zoom_x=2, zoom_y=2, threshold=200):
    cv2_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
    cv2_img = cv2.resize(cv2_img, None, fx=zoom_x, fy = zoom_y, interpolation=cv2.INTER_LINEAR)
    _, cv2_img = cv2.threshold(cv2_img, threshold, 255, cv2.THRESH_BINARY)
    return PIL.Image.fromarray(cv2_img)

# TODO: maybe move to special KISA module
def _find_digit_boxes(pil_image):
    cv2_img = np.array(pil_image)
    _, cv2_img = cv2.threshold(cv2_img, 128, 255, cv2.THRESH_BINARY_INV)
    image, contours, hierarchy = cv2.findContours(cv2_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = []
    for cnt in contours:
        height, width = cv2_img.shape
        rect = utils.add_box_paddings(cv2.boundingRect(cnt), width, height)
        areas.append(Box(*rect))
    areas = sorted(areas, key=lambda box:(box.h),reverse = True)[:12]
    return areas

