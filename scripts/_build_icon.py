import os.path
from PIL import Image


def build_icon(icon_name: str):
    print("| - icon `" + icon_name + "`")
    png_file_name = icon_name + "-256x256.png"
    png_file_path = os.path.join("assets", "icons", png_file_name)
    img = Image.open(png_file_path)
    icon_file_name = icon_name + ".ico"
    icon_file_path = os.path.join("assets", "icons", icon_file_name)
    img.save(icon_file_path)
