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
    throw_feature_not_supported(PLATFORM_NAME, namespace="install", category="platform")


def is_linux() -> bool:
    return PLATFORM_NAME == "Linux"


def is_windows() -> bool:
    return PLATFORM_NAME == "Windows"


def install_common():
    print("install_common")


def install_linux():
    print("install_linux")


def install_windows():
    print("install_windows")


def postinstall_common():
    print("postinstall_common")


def postinstall_linux():
    print("postinstall_linux")


def postinstall_windows():
    print("postinstall_windows")


def preinstall_common():
    print("preinstall_common")


def preinstall_linux():
    print("preinstall_linux")


def preinstall_windows():
    print("preinstall_windows")


def postinstall():
    postinstall_common()
    if is_linux():
        postinstall_linux()
    elif is_windows():
        postinstall_windows()
    else:
        _throw_platform_not_supported()


def preinstall():
    preinstall_common()
    if is_linux():
        preinstall_linux()
    elif is_windows():
        preinstall_windows()
    else:
        _throw_platform_not_supported()


def install():
    preinstall()
    install_common()
    if is_linux():
        install_linux()
    elif is_windows():
        install_windows()
    else:
        _throw_platform_not_supported()
    postinstall()
