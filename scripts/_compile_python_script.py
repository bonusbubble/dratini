import subprocess


def compile_python_script(script_path: str, icon_path: str=None, output_dir: str=None):
    print("| - script `" + script_path + "`")
    command = ["pyinstaller"]
    args = []
    args.append("--onefile")
    args.append("--windowed")
    if icon_path is not None:
        args.append("--icon=" + str(icon_path))
    if output_dir is not None:
        args.append("--distpath=" + output_dir)
    args.append(script_path)
    command.extend(args)
    subprocess.run(command, capture_output=True)
