######################
Clickpecker's Workflow
######################

This part describes how Clickpecker works from inside. It will be usefull for adjusting
algorithms and parameters
for your project or contributing into Clickpecker.

Working with test device via STF utils
======================================

Testing device should be configured for communication via OpenSTF minicap and minitouch.
Check appropriate repositories to find documentation and installation guides
(`minicap <https://github.com/openstf/minicap>`_, `minitouch <https://github.com/openstf/minitouch>`_).

It's highly reccomend to use **Clickpecker Device Manager**, which automates
configuration procees.

Text-based cases: OCR engine
============================

Clickpecker contains OCR engine based on TesseractOCR to find textual UI elements, such
as buttons with labels,
text, headers, etc.
Default recognition process can be divided on several stages:

#. Crop the image to the size specified in config
#. Preprocess the image:

   * Scale image to increase recognition accuracy
   * Binarise image to divide text from background

#. Get boxes of all the words on the screen
#. Postprocess the boxes:

   * Lowercase text, delete spaces and newline characters
   * Replace ligatures
   * Compose words in lines

#. Find and return boxes with contnent similar to wanted

Cropping, parsing, pre- and post- processing parameters can be configured via global
or local configuration.

Image-based cases: template matching
====================================

Clickpecker provides an ability to find images on the screen (e.g. icons and buttons without text) by using
OpenCV pattern matching.

Template image should be loaded and preprocessed (binarised using canny edge detectionon). Also the screenshot is binarised the same way as the template.
Then the template is searched on the differently resized screenshot and
location of the best fit is returned.

This algorithm can't detect if there's no wanted image on the screen.
