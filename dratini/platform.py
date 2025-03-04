import platform

from dratini.utils.error_handling import throw_feature_not_supported as _throw_feature_not_supported


class Platform:
    @property
    def architecture(self):
        architecture = platform.architecture()
        if architecture == "32bit":
            architecture = "i686"
        if architecture == "64bit":
            architecture = "x86_64"
        else:
            _throw_feature_not_supported(architecture, namespace="platform", category="architecture")
        return architecture

    @property
    def name(self):
        return platform.system()


_PLATFORM = Platform()


def get_platform() -> Platform:
    return _PLATFORM


def is_linux() -> bool:
    return get_platform().name == "Linux"


def is_windows() -> bool:
    return get_platform().name == "Windows"
