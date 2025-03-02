import platform
from projectconfig import *


class Platform:
    @property
    def name(self):
        return platform.system()

PLATFORM = Platform()
