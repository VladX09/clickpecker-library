Configuration
=============

Most of API functions can be configured via special config dictionary.

Config merging
--------------
Class :class:`api.BasicAPI` is initialised  by default configuration which can be overrided locally for some methods. If local config is passed to such methods, it will be merged with default config, and merge result will be used. Merged config will not affect other methods.

**Warning!** Base your custom configuration dictionaries on :data:`configurations.default_config` to avoid missing some parameters.


Default config parameters
-------------------------

Here's an example of default config from :data:`configurations`::

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

crop_x_range/crop_y_range
  X and Y axis size-independent bounds for cropping the screenshot.
  Value: a pair of real numbers from 0 to 1.

api_scroll_repeats
  Used in :meth:`api.BasicAPI.scroll_for`. Maximum number of unsuccessfull scrolls before raising the exception

api_wait_timeout
  Used in :meth:`api.BasicAPI.wait_for` and. Maximum wait timeout before raising the exception.

api_tap_timeout
  Same as :data:`api_wait_timeout` but used in :meth:`api.BasicAPI.tap`.

api_tap_index
  Specifies which element occurrence will be chosen if several were found.

api_similarity_fun
  Specifies method of images comparsion inside API functions.  

device_wrapper_similarity_fun
  Specifies method of images comparsion during logging screenshot history.

api_similarity_threshold / device_wrapper_similarity_threshold
  Thresholds for appropriate similarity functions.

ocr_preprocessing
  Image preprocessing function for OCR engine.

ocr_postprocessing
  Function for postprocessing restults of OCR parsing.

ocr_similarity_cutoff
  Helps to smooth recognition errors. Value: a number from 0 to 100.

ocr_GetComponentImages_params
  :meth:`tesserocr.PyTessBaseAPI.GetComponentImages` parameters.

ocr_PyTessBaseAPI_params
  :meth:`tesserocr.PyTessBaseAPI` constructor parameters.
