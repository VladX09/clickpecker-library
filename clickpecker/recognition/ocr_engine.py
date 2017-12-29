import functools

from tesserocr import PyTessBaseAPI, RIL, PSM
from fuzzywuzzy import fuzz, process

from clickpecker.processing import image_processing, boxes_processing, utils
from clickpecker.models.immutable import Box, ContentBox


def _prepare_boxes(api, image, config):
    GetComponentImages_params = config["ocr_GetComponentImages_params"]
    component_images = api.GetComponentImages(**GetComponentImages_params)
    boxes = [Box(**box) for (_, box, _, _) in component_images]
    width, height = image.size
    boxes = [utils.add_box_paddings(box, width, height) for box in boxes]
    boxes = utils.filter_parent_boxes(boxes)
    return boxes


def _get_content_boxes(image, config, predefined_boxes=None):
    PyTessBaseAPI_params = config["ocr_PyTessBaseAPI_params"]
    with PyTessBaseAPI(**PyTessBaseAPI_params) as api:
        api.SetImage(image)
        width, height = image.size
        if predefined_boxes == None:
            areas = _prepare_boxes(api, image, config)
        else:
            areas = predefined_boxes
        areas = [
            box for box in areas
            if functools.reduce(lambda d1, d2: d1 > 0 and d2 > 0, box)
        ]
        boxes = []
        for i, box in enumerate(areas):
            api.SetRectangle(box.x, box.y, box.w, box.h)
            text = api.GetUTF8Text()
            conf = api.MeanTextConf()
            boxes.append(ContentBox(text, box))
        return utils.abs_to_rel(boxes, width, height)


def parse(image, config):

    x_range = config["crop_x_range"]
    y_range = config["crop_y_range"]
    preproc = config["ocr_preprocessing"]
    postproc = config["ocr_postprocessing"]

    # x_range and y_range are tuples (min, max), where min and max are from 0 to 1
    w, h = image.size
    cropped_img = image.crop((x_range[0] * w, y_range[0] * h, x_range[1] * w,
                              y_range[1] * h))
    crop_w, crop_h = cropped_img.size

    preprocesssed_img = preproc(cropped_img)
    boxes = _get_content_boxes(preprocesssed_img, config)
    postprocessed_boxes = postproc(boxes)

    # Transform box coordinates to fit original image
    return utils.rebase_box(postprocessed_boxes, x_range[0], y_range[0],
                            crop_w, crop_h, w, h)


def search_on_image(image, text, config):

    cutoff = config["ocr_similarity_cutoff"]

    def find_best(boxes):
        best_fit = process.extractOne(
            text, [box.content for box in boxes],
            scorer=fuzz.UWRatio,
            score_cutoff=cutoff)

        if (best_fit is not None):
            boxes = [box for box in boxes if box.content == best_fit[0]]
        else:
            boxes = []
        return boxes

    boxes = parse(image, config)
    best_fit = find_best(boxes)
    return best_fit
