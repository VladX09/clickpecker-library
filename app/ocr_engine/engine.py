from PIL import Image
from . import postprocessing, preprocessing, utils
from tesserocr import PyTessBaseAPI, RIL, PSM
from ..datatypes import Box, ContentBox
import numpy as np

def get_content_boxes(image,
                      level=RIL.WORD, text_only=False,
                      predefined_boxes=None,
                      psm=PSM.AUTO, **api_params):
    with PyTessBaseAPI(psm=psm) as api:
        api.SetImage(image)
        width, height = image.size
        if predefined_boxes == None:
            areas = _prepare_boxes(api, image, level=level, text_only=text_only, **api_params)
        else:
            areas = predefined_boxes
        boxes = []
        for i, box in enumerate(areas):
            api.SetRectangle(box.x, box.y, box.w, box.h)
            text = api.GetUTF8Text()
            conf = api.MeanTextConf()
            boxes.append(ContentBox(text, box))
        return utils.abs_to_rel(boxes, width, height)

def _prepare_boxes(api, image, **api_params):
    component_images = api.GetComponentImages(**api_params)
    boxes = [Box(**box) for (_,box,_,_) in component_images]
    width, height = image.size
    boxes = [utils.add_box_paddings(box, width, height) for box in boxes]
    boxes = utils.filter_parent_boxes(boxes)
    return boxes

def basic_parse(image,
                preproc_fun=preprocessing.binary,
                postproc_fun=postprocessing.basic_postprocessing,
                **gcb_params):
    image = preproc_fun(image)
    boxes = get_content_boxes(image, **gcb_params)
    boxes = postproc_fun(boxes)
    return boxes

def crop_parse(image, x_range, y_range, **basic_parse_params):
    # x_range and y_range are tuples (min, max), where min and max are from 0 to 1
    w, h = image.size
    cropped_img = image.crop((x_range[0] * w, y_range[0] * h,
                              x_range[1] * w, y_range[1] * h))
    crop_w, crop_h = cropped_img.size
    boxes = basic_parse(cropped_img, **basic_parse_params)

    # Transform box coordinates to fit original image
    return utils.rebase_box(boxes, x_range[0], y_range[0], crop_w, crop_h, w, h)
