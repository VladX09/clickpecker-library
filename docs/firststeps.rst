###########
First Steps
###########

Requirements
============

Clickpecker requires:

libtesseract (tested on 3.04) and libleptonica (>= 1.71)
    In Ubuntu::

      $ apt-get install tesseract-ocr libtesseract-dev libleptonica-dev

    For more information check out `tesserocr repo <https://github.com/sirfz/tesserocr>`_.

Android Debug Bridge (ADB)
    Path to ADB binary should be in ``$PATH`` variable.

OpenSTF minicap and minitouch
    Should be launched on testing devices.
    For more information check out `minicap <https://github.com/openstf/minicap>`_
    and `minitouch <https://github.com/openstf/minitouch>`_ repos.

To make installing minicap/minitouch and obtaining devices easier, run
**Clickpecker Device Manager server**.

Installation
============

Install Clickpecker library from source::

    pip install git+https://github.com/VladX09/clickpecker-library.git

Getting Started
===============

**Warning!** This version uses only template matching with pyramid representation for
image-based cases (e.g. finding and tapping icons). This method is robust to differences in
size and resolution of the template icon and device's screen. But it has got it's own drawbacks.
Current template matcher hasn't got any thresholds and it can't detect if there's no wanted
image on the screen. That's why some methods (e.g. ``search``, ``wait_for``, ``scroll_for``)
aren't accept images.

The main object of Clickpecker is :class:`clickpecker.BasicAPI`. To init API, you should have
`DeviceWrapper` object and a dictionary with the default configuration.

.. code-block:: python

   from clickpecker import BasicAPI
   from clickpecker.models import Device
   from clickpecker.helpers import DeviceWrapper
   from clickpecker.configurations import default_config

   device = Device(adb_id = "device_adb_id",
                device_name = "Testing Device",
                android_version = "8.0",
                minicap_port = 1111,
                minitouch_port = 1112)

   device_wrapper = DeviceWrapper(device)
   api = BasicAPI(device_wrapper, default_config)

If your device is connected, visible by ADB and has got minicap and minitouch
launched on appropriate ports, you can start work with it.

Send ADB command::

  api.adb("shell pm clear com.your.app")

Tap **Next** button on device's screen::

  api.tap("Next")

Wait for **OK** button appears::

  api.wait_for("OK")

Scroll down (swipe from the first relative (X,Y) point to the second one)
till **Next** button appears::

  api.scroll_for("Next", (0.5, 0.6), (0.5, 0.2))


Tap **icon** on device's screen (via template_matching)::

  from clickpecker.recognition import tm_engine

  icon = tm_engine.load_template("icon.png")
  api.tap(icon)


Wait for **OK** button appears in the specific region. Region is set by it's
relative X and Y bounds::

  api.tap(
      "OK",
      config=dict(
          api_tap_timeout=60 * 5, # Wait for 5 minutes
          crop_x_range=(0.1, 0.9),
          crop_y_range=(0.4, 0.8)))

Assertions
==========
Clickpecker provides different methods to make assertions about
the state of an application under testing. These methods are based
on the human way of visual observing.

First of all, text-based UI assertions can be made by
:meth:`clickpecker.BasicAPI.search` method::

    assert len(api.search("OK")) != 0  # Assert OK button presents on screen

Also there are methods to assert that device's screen should (or shouldn't)
change after some actions::
 
    with api.assert_screen_change()
        api.tap("OK")


    import time
    with api.assert_screen_same()
        time.sleep(50)
    
In common case, it's possible to compare current screenshot with the
previously saved one::

    tag = "State 1"
    api.save_current_screen(tag)
    # do something
    assert api.screen_similar_with(tag)
