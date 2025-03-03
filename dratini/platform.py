import platform


class Platform:
    @property
    def name(self):
        return platform.system()


_PLATFORM = Platform()


def is_linux() -> bool:
    return _PLATFORM.name == "Linux"


def is_windows() -> bool:
    return _PLATFORM.name == "Windows"
