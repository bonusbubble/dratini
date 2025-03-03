#!/usr/bin/env python3

import os
import shutil
import subprocess

from dratini.utils import is_linux, is_windows, throw_feature_not_supported

from .config import *
from .uninstall import uninstall, uninstall_dir, uninstall_file


#-----------#
# Functions #
#-----------#

def _throw_platform_not_supported():
    throw_feature_not_supported(PLATFORM_NAME, namespace="install", category="platform")


def _install_common():
    pass


def _install_linux():
    _install_linux__chmod_bin()
    _install_linux__copy_lib()
    _install_linux__link_main_executable()


def _install_linux__chmod_bin():
    subprocess.run([ "chmod", "+x", BIN_PATH ])


def _install_linux__copy_lib():
    copy_dest_path = os.path.join(INSTALL_LIB_DIR, PROJECT.name)
    shutil.copytree(".", copy_dest_path)


def _install_linux__link_main_executable():
    ln_src_path = os.path.join(INSTALL_LIB_DIR, PROJECT.name, BIN_PATH)
    ln_dest_path = os.path.join(INSTALL_BIN_DIR, PROJECT.name)
    subprocess.run([ "ln", "-s", ln_src_path, ln_dest_path ])


def _install_windows():
    _install_windows__copy_lib()
    _install_windows__link_main_executable()


def _install_windows__copy_lib():
    copy_dest_path = os.path.join(INSTALL_LIB_DIR, PROJECT.name)
    uninstall_dir(copy_dest_path)
    shutil.copytree(".", copy_dest_path)


def _install_windows__link_main_executable():
    ln_src_path = os.path.join(INSTALL_LIB_DIR, PROJECT.name, BIN_PATH)
    ln_dest_path = os.path.join(INSTALL_BIN_DIR, PROJECT.name)
    uninstall_file(ln_dest_path)
    shutil.copy(ln_src_path, ln_dest_path)


def _postinstall_common():
    pass


def _postinstall_linux():
    pass


def _postinstall_windows():
    pass


def _preinstall_common():
    pass


def _preinstall_linux():
    pass


def _preinstall_windows():
    pass


def _postinstall():
    _postinstall_common()
    if is_linux():
        _postinstall_linux()
    elif is_windows():
        _postinstall_windows()
    else:
        _throw_platform_not_supported()


def _preinstall():
    _preinstall_common()
    if is_linux():
        _preinstall_linux()
    elif is_windows():
        _preinstall_windows()
    else:
        _throw_platform_not_supported()


def install():
    uninstall()
    _preinstall()
    _install_common()
    if is_linux():
        _install_linux()
    elif is_windows():
        _install_windows()
    else:
        _throw_platform_not_supported()
    _postinstall()
