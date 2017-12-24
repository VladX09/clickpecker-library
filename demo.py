from clickpecker.helpers.device_wrappers import DeviceWrapper
from clickpecker.recognition import tm_engine
from clickpecker.api import BasicAPI



def test_demo():
    device_spec = {
        "adb_id": "BL4B22D10786",
    }
    device_manager_url = "http://127.0.0.1:5000"

    device_wrapper = DeviceWrapper.obtain_by_device_manager(
        device_spec, device_manager_url)
    settings_ico = tm_engine.load_template("tm_img/settings_ico.png")
    api = BasicAPI(device_wrapper)
    api.adb("shell pm clear com.kms.free")
    # Способ запуска приложения без указания Activity
    api.adb("shell monkey -p com.kms.free 1")
    api.tap("accept and continue")
    api.wait_for("activation code")
    api.scroll_for("use free version", (0.5, 0.6), (0.5, 0.2))
    api.tap("use free version")
    api.tap("run the scan")
    # Эта команда вырежет участок из нижней половины скриншота
    # Чтобы распознать злосчастную кнопку ОК
    api.tap("OK", 60 * 5, crop_x_range=(0.1, 0.9), crop_y_range=(0.4, 0.8))
    api.tap("rate later")
    api.tap(settings_ico)
    api.tap("additional")
    api.tap("get notifications about")
    api.tap("get sound")
