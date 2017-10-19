from app import tm_engine
from app.device import Device

if __name__ == "__main__":

    cap_addr = ("", 1313)
    touch_addr = ("", 1111)
    adb_id = "BL4B22D10786"
    dev = Device(cap_addr, touch_addr, adb_id)

    settings_ico = tm_engine.load_template("tm_img/settings_ico.png")

    dev.adb("shell pm clear com.kms.free")
    # Способ запуска приложения без указания Activity
    dev.adb("shell monkey -p com.kms.free 1")
    dev.tap("accept and continue")
    dev.tap("use free version")
    dev.tap("run the scan")
    # Эта команда вырежет участок из нижней половины скриншота
    # Чтобы распознать злосчастную кнопку ОК
    dev.tap("OK", 60 * 5, x_range=(0.1, 0.9), y_range=(0.4, 0.8))
    dev.tap("rate later")
    dev.tap_img(settings_ico)
    dev.tap("additional")
    dev.tap("get notifications about")
    dev.tap("get sound")

