import os

from _build_icon import build_icon

from _compile_python_script import compile_python_script


def build_subproject(name: str):
    print("- subproject `" + name + "`")
    script_path = name + ".py"
    build_icon(name)
    compile_python_script(
            script_path,
            icon_path=os.path.join("assets", "icons", name + ".ico"),
            output_dir="bin"
    )
