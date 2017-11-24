import numpy as np
import cv2
from PIL import Image

from app.datatypes import Box


def load_template(path):
    cv2_img = cv2.imread(path)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    cv2_img = cv2.Canny(cv2_img, 50, 200)
    return Image.fromarray(cv2_img)


def get_match(image, template):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    template = np.array(template)
    t_w, t_h = template.shape[::-1]
    found = None

    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = cv2.resize(
            image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        r_w, r_h = resized.shape[::-1]
        if (r_w < t_w) or (r_h < t_h):
            break
        edged = cv2.Canny(resized, 50, 200)
        res = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
        (_, max_val, _, max_loc) = cv2.minMaxLoc(res)
        if found is None or max_val > found[0]:
            max_loc = (max_loc[0] / r_w, max_loc[1] / r_h, t_w / r_w,
                       t_h / r_h)
            found = (max_val, max_loc)

    max_val, max_loc = found
    box = Box(*max_loc)
    return box
