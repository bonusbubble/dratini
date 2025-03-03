#!/usr/bin/env python3

import importlib.util
import os
import platform
import shutil
import sys
import tempfile
import urllib.request


_PROJECT_NAME: str = "dratini"

_PROJECT_MODULE_INSTANCE__EMPTY = ""
_PROJECT_MODULE_INSTANCE: any = _PROJECT_MODULE_INSTANCE__EMPTY

_PLATFORM_NAME: str = platform.system()


def project_name() -> str:
    return _PROJECT_NAME


def project_entry_point(archive_path: str) -> str:
    return os.path.join(archive_path, project_name() + ".py")


def dratini(archive_path: str) -> any:
    instance = _PROJECT_MODULE_INSTANCE
    if instance is _PROJECT_MODULE_INSTANCE__EMPTY:
        module_name = _PROJECT_NAME
        module_dir_list = [archive_path]
        spec = importlib.machinery.PathFinder().find_spec(module_name, module_dir_list)
        instance = spec.loader.load_module(module_name)
    return instance


def is_linux() -> bool:
    return _PLATFORM_NAME == "Linux"


def is_windows() -> bool:
    return _PLATFORM_NAME == "Windows"


def abort(message: any):
    print("Error: " + str(message))
    exit(1)


def install_root():
    if is_linux():
        return "/usr/local/lib"
    if is_windows():
        return "C:\\Program Files"
    abort("Platform not yet supported: " + platform_name)


def install_dir():
    return os.path.join(install_root(), project_name())


def download_file(url: str, file_path: str):
    urllib.request.urlretrieve(url, file_path)


def download_branch(branch: str="main", tmp_dir: str="") -> str:
    if tmp_dir is None or len(tmp_dir) < 1:
        tmp_dir = tempfile.gettempdir()
    print("Downloading latest release...")
    archive_url = "https://github.com/bonusbubble/dratini/archive/refs/heads/" + branch + ".zip"
    archive_name = "dratini-" + branch
    archive_path = os.path.join(tmp_dir, archive_name)
    zip_archive_path = archive_path + ".zip"
    download_file(archive_url, zip_archive_path)
    unzip_archive_path = archive_path + "__unzip"
    shutil.unpack_archive(zip_archive_path, unzip_archive_path)
    unzipped_archive_path = os.path.join(unzip_archive_path, archive_name)
    shutil.move(unzipped_archive_path, archive_path)
    os.remove(zip_archive_path)
    shutil.rmtree(unzip_archive_path)
    return archive_path


def install_archive(archive_path: str):
    dratini(archive_path).installer.install()

import time

def install():
    with tempfile.TemporaryDirectory() as tmp_dir:
        archive_path = download_branch("main", tmp_dir=tmp_dir)
        install_archive(archive_path)


install()
