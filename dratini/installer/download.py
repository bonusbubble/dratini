from dragonegg import download_file
from dratini.platform import get_platform, is_linux, is_windows


def download_raylib():
    if is_windows():

        archive_url = "https://github.com/raysan5/raylib/releases/download/5.5/raylib-5.5_win64_mingw-w64.zip"
    archive_path = "raylib.zip"
    download_file(archive_url, archive_path)
