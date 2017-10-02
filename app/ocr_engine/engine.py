from PIL import Image
from . import postprocessing, preprocessing, utils
from tesserocr import PyTessBaseAPI, RIL, PSM
from ..namedtuples import Box, ContentBox
import numpy as np

#TODO: move api settings into **kwargs
def get_content_boxes(image, level=RIL.WORD, text_only=False,
                     raw_image=False, predefined_areas=None,
                     psm=PSM.AUTO):
    with PyTessBaseAPI(psm=psm) as api:
        api.SetImage(image)
        if predefined_areas == None:
            areas = _prepare_areaes(api, image, level=level, text_only=text_only, raw_image=raw_image)
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

def _prepare_areaes(api, image, **api_params):
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
    # TODO: add postprocessing: create lines and return center coordinates
    return boxes

# TODO: add crop_parse
