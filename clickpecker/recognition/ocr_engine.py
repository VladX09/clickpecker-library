import functools

from tesserocr import PyTessBaseAPI, RIL, PSM
from fuzzywuzzy import fuzz, process

from clickpecker.processing import image_processing, boxes_processing, utils
from clickpecker.models.immutable import Box, ContentBox


def _prepare_boxes(api, image, **api_params):
    component_images = api.GetComponentImages(**api_params)
    boxes = [Box(**box) for (_, box, _, _) in component_images]
    width, height = image.size
    boxes = [utils.add_box_paddings(box, width, height) for box in boxes]
    boxes = utils.filter_parent_boxes(boxes)
    return boxes


def _get_content_boxes(image,
                       level=RIL.WORD,
                       text_only=False,
                       predefined_boxes=None,
                       psm=PSM.AUTO,
                       **api_params):
    with PyTessBaseAPI(psm=psm) as api:
        api.SetImage(image)
        width, height = image.size
        if predefined_boxes == None:
            areas = _prepare_boxes(
                api, image, level=level, text_only=text_only, **api_params)
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


def parse(image,
          x_range=(0, 1),
          y_range=(0, 1),
          preproc=image_processing.binary_thresholder(
              zoom_x=2, zoom_y=2, threshold=200),
          postproc=boxes_processing.basic_postprocessing,
          **gcb_params):

    # x_range and y_range are tuples (min, max), where min and max are from 0 to 1
    w, h = image.size
    cropped_img = image.crop((x_range[0] * w, y_range[0] * h, x_range[1] * w,
                              y_range[1] * h))
    crop_w, crop_h = cropped_img.size

    preprocesssed_img = preproc(cropped_img)
    boxes = _get_content_boxes(preprocesssed_img, **gcb_params)
    postprocessed_boxes = postproc(boxes)

    # Transform box coordinates to fit original image
    return utils.rebase_box(postprocessed_boxes, x_range[0], y_range[0],
                            crop_w, crop_h, w, h)


def search_on_image(image, text, x_range=(0, 1), y_range=(0, 1),
                    similarity=90):
    boxes = parse(image, x_range, y_range)
    best_fit = process.extractOne(
        text, [box.content for box in boxes],
        scorer=fuzz.UWRatio,
        score_cutoff=similarity)
    if (best_fit is not None):
        # print("best_fit: ", best_fit)
        boxes = [box for box in boxes if box.content == best_fit[0]]
    else:
        boxes = []
    return boxes
