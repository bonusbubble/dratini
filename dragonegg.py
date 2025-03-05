#!/usr/bin/env python3

import argparse
import importlib.machinery
import importlib.util
import os
import platform
import shutil
import sys
import tempfile
import time
import urllib.request


_PROJECT_NAME: str = "dratini"

_PROJECT_MODULE_INSTANCE__EMPTY = ""
_PROJECT_MODULE_INSTANCE: any = _PROJECT_MODULE_INSTANCE__EMPTY

_PLATFORM_NAME: str = platform.system()


_HATCH_EXCEPTION_MESSAGE = " ".join([
        "The egg was unable to hatch at the current time.",
        "Please make sure you running `dragonegg` as an administrator."
])

_LAY_EXCEPTION_MESSAGE = " ".join([
        "The egg could not be laid at the requested location.",
        "Please make sure you running `dragonegg` as an administrator if installing globally."
])


def _get_dratini_system_path_entry(nest: str) -> str:
    return os.path.join(nest, "bin")


class HatchException(Exception):
    def __init__(self, egg: str, nest: str):
        super().__init__(_HATCH_EXCEPTION_MESSAGE)
        self.egg = egg
        self.nest = nest


class LayException(Exception):
    def __init__(self, nest: str):
        super().__init__(_LAY_EXCEPTION_MESSAGE)
        self.nest = nest


def platform_name():
    return _PLATFORM_NAME


def project_name() -> str:
    return _PROJECT_NAME


def project_entry_point(archive_path: str) -> str:
    return os.path.join(archive_path, project_name() + ".py")


def get_system_path() -> (str | None):
    system_path = None
    if os.name == "nt":
        import winreg
        # Get the current user registry.
        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
            # Go to the environment key.
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                # Grab the current path value.
                system_path = winreg.QueryValueEx(key, "PATH")[0]
    else:
        system_path = os.environ.get("PATH")
    return system_path


def append_to_system_path(program_path:str, verbose: bool=False):
    """Takes in a path to a program and adds it to the system path"""
    if os.name == "nt": # Windows systems
        import ctypes # Allows interface with low-level C API's
        import winreg # Allows access to the windows registry

        # Get the current user registry.
        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
            # Go to the environment key.
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                # Grab the current path value.
                existing_path_value = winreg.QueryValueEx(key, "PATH")[0]
                # Take the current path value and append the new program path.
                new_path_value = existing_path_value + ";" + program_path
                # Updated the path with the updated path.
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value)

            # Tell other processes to update their environment.
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x1A
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_long()
            SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
            SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u"Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(result),)
    # If system is *nix.
    else:
        # Open bashrc file.
        bash_export_line = f'export PATH="{program_path}:$PATH"'
        with open(f"{os.getenv('HOME')}/.bashrc", "r") as bash_file:
            bash_file_contents = bash_file.read().strip().split("\n")
            if bash_export_line in bash_file_contents:
                return
        with open(f"{os.getenv('HOME')}/.bashrc", "a") as bash_file:
            # Add program path to Path variable.
            bash_file.write("\n" + bash_export_line + "\n")
        # Update bash source.
        os.system(f". {os.getenv('HOME')}/.bashrc")
    if verbose:
        print(f"Added {program_path} to the system path; please restart shell for changes to take effect.")


def add_dratini_to_system_path(nest: str):
    original_system_path = get_system_path().split(";")
    dratini_system_path_entry = _get_dratini_system_path_entry(nest)
    if dratini_system_path_entry not in original_system_path:
        append_to_system_path(dratini_system_path_entry)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            prog="dragonegg",
            description="The Official Dratini Installer",
            epilog="Copyright (c) 2025 bonusbyte.org",
            usage="dragonegg [--hatch DRATINI_ROOT]"
    )
    parser.add_argument(
            "-e",
            "--egg",
            type=str,
            default="",
            required=False
    )
    parser.add_argument(
            "--hatch",
            action="store_true",
            help="hatch (install) an egg (Dratini `.zip`) into a nest (installation directory)"
    )
    parser.add_argument(
            "--lay",
            action="store_true",
            help="lay (install) an egg (Dratini `.zip`) into a nest (download directory)"
    )
    parser.add_argument(
            "-n",
            "--nest",
            type=str,
            default=install_dir(),
            required=False
    )
    args = parser.parse_args()
    return args


def dratini(archive_path: str) -> any:
    instance = _PROJECT_MODULE_INSTANCE
    if instance is _PROJECT_MODULE_INSTANCE__EMPTY:
        module_name = _PROJECT_NAME
        module_dir_list = [archive_path]
        spec = importlib.machinery.PathFinder().find_spec(module_name, module_dir_list)
        instance = spec.loader.load_module(module_name)
    return instance


def is_linux() -> bool:
    return platform_name() == "Linux"


def is_windows() -> bool:
    return platform_name() == "Windows"


def abort(message: any):
    print("Error: " + str(message))
    exit(1)


def install_root():
    if is_linux():
        return "/usr/local/lib"
    if is_windows():
        return "C:\\Program Files"
    abort("Platform not yet supported: " + platform_name())


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
    archive_git_dir = os.path.join(unzipped_archive_path, ".git")
    if os.path.exists(archive_git_dir):
        shutil.rmtree(archive_git_dir)
    shutil.move(unzipped_archive_path, archive_path)
    os.remove(zip_archive_path)
    shutil.rmtree(unzip_archive_path)
    return archive_path


def install_archive(egg: str, nest: str):
    # TODO: Use `nest` in `installer.install` and `installer.uninstall`.
    dratini(egg).installer.uninstall()
    dratini(egg).installer.install()


def _hatch(egg: str, nest: str):
    if os.path.exists(egg):
        install_archive(egg, nest)
    else:
        with tempfile.TemporaryDirectory() as tmp_dir:
            archive_path = download_branch("main", tmp_dir=tmp_dir)
            install_archive(archive_path, nest)
    add_dratini_to_system_path(nest)


def hatch(egg: str, nest: str):
    try:
        _hatch(egg, nest)
    except:
        raise HatchException(egg, nest)


def _lay(nest: str):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_egg = download_branch("main", tmp_dir=tmp_dir)
        shutil.move(tmp_egg, args.nest)


def lay(nest: str):
    try:
        _lay(nest)
    except:
        raise LayException(nest)


args = parse_args()

if args.lay:
    try:
        _lay(args.nest)
    except LayException as error:
        abort(str(error))

if args.hatch or (not args.lay):
    try:
        _hatch(args.egg, args.nest)
    except HatchException as error:
        abort(str(error))
