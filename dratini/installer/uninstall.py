#!/usr/bin/env python3

import os
import shutil

from dratini.utils import is_linux, is_windows, throw_feature_not_supported

from .config import *


#-----------#
# Functions #
#-----------#

def _throw_platform_not_supported():
    throw_feature_not_supported(PLATFORM_NAME, namespace="uninstall", category="platform")


def uninstall_dir(dir_path: str) -> bool:
    try:
        if os.path.exists(dir_path):
            return False
        shutil.rmtree(dir_path, ignore_errors=True)
        return True
    except:
        return False
    return False


def uninstall_file(file_path: str) -> bool:
    try:
        if os.path.exists(file_path):
            return False
        os.remove(file_path)
        return True
    except:
        return False
    return False


def _uninstall_common():
    pass


def _uninstall_linux():
    _uninstall_linux__copy_lib()
    _uninstall_linux__link_main_executable()


def _uninstall_linux__copy_lib():
    copy_dest_path = os.path.join(INSTALL_LIB_DIR, PROJECT.name)
    if os.path.exists(copy_dest_path):
        shutil.rmtree(copy_dest_path)


def _uninstall_linux__link_main_executable():
    ln_dest_path = os.path.join(INSTALL_BIN_DIR, PROJECT.name)
    uninstall_file(ln_dest_path)


def _uninstall_windows():
    _uninstall_windows__copy_lib()
    _uninstall_windows__link_main_executable()


def _uninstall_windows__copy_lib():
    copy_dest_path = os.path.join(INSTALL_LIB_DIR, PROJECT.name)
    if os.path.exists(copy_dest_path):
        shutil.rmtree(copy_dest_path)

def _uninstall_windows__link_main_executable():
    ln_dest_path = os.path.join(INSTALL_BIN_DIR, PROJECT.name)
    uninstall_file(ln_dest_path)


def _postuninstall_common():
    pass


def _postuninstall_linux():
    pass


def _postuninstall_windows():
    pass


def _preuninstall_common():
    pass


def _preuninstall_linux():
    pass


def _preuninstall_windows():
    pass


def _postuninstall():
    _postuninstall_common()
    if is_linux():
        _postuninstall_linux()
    elif is_windows():
        _postuninstall_windows()
    else:
        _throw_platform_not_supported()


def _preuninstall():
    _preuninstall_common()
    if is_linux():
        _preuninstall_linux()
    elif is_windows():
        _preuninstall_windows()
    else:
        _throw_platform_not_supported()


def uninstall():
    _preuninstall()
    _uninstall_common()
    if is_linux():
        _uninstall_linux()
    elif is_windows():
        _uninstall_windows()
    else:
        _throw_platform_not_supported()
    _postuninstall()
