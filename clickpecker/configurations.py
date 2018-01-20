from functools import partial
from clickpecker.processing.image_processing import basic_binarisation, check_mse_similar, check_ssim_similar
from clickpecker.processing.boxes_processing import basic_postprocessing
from tesserocr import PyTessBaseAPI, RIL, PSM

ssim = partial(check_ssim_similar, multichannel=True)

default_config = {
    "crop_x_range": (0, 1),
    "crop_y_range": (0, 1),
    "api_scroll_repeats": 3,
    "api_wait_timeout": 60,
    "api_tap_timeout": 60,
    "api_tap_index": 0,
    "api_similarity_fun": check_mse_similar,
    "api_similarity_threshold": 20,
    "device_wrapper_similarity_fun": ssim,
    "device_wrapper_similarity_threshold": 0.9,
    "ocr_preprocessing": basic_binarisation(),
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
