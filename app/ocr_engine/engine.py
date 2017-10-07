from PIL import Image
from . import postprocessing, preprocessing, utils
from tesserocr import PyTessBaseAPI, RIL, PSM
from ..datatypes import Box, ContentBox
import numpy as np

def get_content_boxes(image,
                      level=RIL.WORD, text_only=False,
                      predefined_areas=None,
                      psm=PSM.AUTO, **api_params):
    with PyTessBaseAPI(psm=psm) as api:
        api.SetImage(image)
        if predefined_areas == None:
            areas = _prepare_areas(api, image, level=level, text_only=text_only, **api_params)
        else:
            areas = predefined_areas
        boxes = []
        for i, box in enumerate(areas):
            api.SetRectangle(box.x, box.y, box.w, box.h)
            text = api.GetUTF8Text()
            conf = api.MeanTextConf()
            boxes.append(ContentBox(text, box))
            # print (u"Box[{0}]: x={box.x}, y={box.y}, w={box.w}, h={box.h}, confidence: {1}, text: {2}"
            #        .format(i, conf, text, box=box).encode("utf-8"))
        return boxes

def _prepare_areas(api, image, **api_params):
    component_images = api.GetComponentImages(**api_params)
    areas = [[box['x'], box['y'], box['w'], box['h']] for (_,box,_,_) in component_images]
    width, height = image.size
    areas = [utils.add_box_paddings(area, width, height) for area in areas]
    areas = [Box(*area) for area in areas]
    areas = utils.filter_parent_boxes(areas)
    return areas

def basic_parse(image,
                preproc_fun=preprocessing.binary,
                postproc_fun=postprocessing.basic_postprocessing,
                **gcb_params):
    image = preproc_fun(image)
    boxes = get_content_boxes(image, **gcb_params)
    boxes = postproc_fun(boxes)
    return boxes

def crop_parse(image, x_range, y_range, **basic_parse_params):
    width, height = image.size
    cropped_img = image.crop((x_range[0] * width, y_range[0] * height,
                              x_range[1] * width, y_range[1] * height))
    boxes = basic_parse(cropped_img, **basic_parse_params)

    # Transform box coordinates to fit original image
    scaled_boxes = [ContentBox(box.content, Box(box.position.x + width * x_range[0],
                                            box.position.y + height * y_range[0],
                                            box.position.w, box.position.h)) for box in boxes]
    return scaled_boxes
