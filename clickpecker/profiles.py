from clickpecker.processing.image_processing import binary_thresholder
from clickpecker.processing.boxes_processing import basic_postprocessing
from tesserocr import PyTessBaseAPI, RIL, PSM

default_config = {
    "crop_x_range": (0, 1),
    "crop_y_range": (0, 1),
    "api_scroll_repeats": 3,
    "api_wait_timeout": 60,
    "api_tap_timeout": 60,
    "api_tap_index": 0,
    "ocr_preprocessing": binary_thresholder(),
    "ocr_postprocessing": basic_postprocessing,
    "ocr_similarity_cutoff": 90,
    "ocr_GetComponentImages_params": {
        "level": RIL.WORD,
        "text_only": False
    },
    "ocr_PyTessBaseAPI_params": {
        "psm": PSM.AUTO
    }
}
