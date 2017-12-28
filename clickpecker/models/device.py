from packaging import version
 
class Device:
    def __init__(self,
                 adb_id=None,
                 device_name=None,
                 status=None,
                 android_version=None,
                 sdk_version=None,
                 minicap_port=None,
                 minitouch_port=None,
                 stf_address=None):
        self.adb_id = adb_id
        self.device_name = device_name
        self.status = status
        self.android_version = android_version
        self.sdk_version = sdk_version
        self.minicap_port = minicap_port
        self.minitouch_port = minitouch_port
        self.stf_address = stf_address

    @property
    def android_version(self):
        return self._android_version

    @android_version.setter
    def android_version(self, value):
        self._android_version = None if value is None else version.parse(value)

    @classmethod
    def from_dict(cls, dict):
        allowed = ("adb_id", "device_name", "status", "android_version",
                   "sdk_version", "minicap_port", "minitouch_port",
                   "stf_address")
        args = {k: v for k, v in dict.items() if k in allowed}
        return cls(**args)

    def to_dict(self):
        data = dict(self.__dict__)
        data["android_version"] = str(data.pop("_android_version", None))
        return data

    def __repr__(self):
        return repr(self.__dict__)
