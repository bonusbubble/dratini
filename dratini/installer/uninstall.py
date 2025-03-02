#!/usr/bin/env python3

import os
import platform

from ..utils import throw_feature_not_supported


#-----------#
# Variables #
#-----------#

PLATFORM_NAME = platform.system()


#-----------#
# Functions #
#-----------#

def _throw_platform_not_supported():
    throw_feature_not_supported(PLATFORM_NAME, namespace="uninstall", category="platform")


def is_linux() -> bool:
    return PLATFORM_NAME == "Linux"


def is_windows() -> bool:
    return PLATFORM_NAME == "Windows"


def uninstall_common():
    print("uninstall_common")


def uninstall_linux():
    print("uninstall_linux")


def uninstall_windows():
    print("uninstall_windows")


def postuninstall_common():
    print("postuninstall_common")


def postuninstall_linux():
    print("postuninstall_linux")


def postuninstall_windows():
    print("postuninstall_windows")


def preuninstall_common():
    print("preuninstall_common")


def preuninstall_linux():
    print("preuninstall_linux")


def preuninstall_windows():
    print("preuninstall_windows")


def postuninstall():
    postuninstall_common()
    if is_linux():
        postuninstall_linux()
    elif is_windows():
        postuninstall_windows()
    else:
        _throw_platform_not_supported()


def preuninstall():
    preuninstall_common()
    if is_linux():
        preuninstall_linux()
    elif is_windows():
        preuninstall_windows()
    else:
        _throw_platform_not_supported()


def uninstall():
    preuninstall()
    uninstall_common()
    if is_linux():
        uninstall_linux()
    elif is_windows():
        uninstall_windows()
    else:
        _throw_platform_not_supported()
    postuninstall()
