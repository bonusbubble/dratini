import platform


class Platform:
    @property
    def name(self):
        return platform.system()

PLATFORM = Platform()
