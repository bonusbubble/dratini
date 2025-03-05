import subprocess


def install_dev_dependencies(pip: str):
    command = [pip]
    args = []
    dev_dependencies = [ "Pillow", "pyinstaller" ]
    args.append("install")
    args.extend(dev_dependencies)
    command.extend(args)
    results = subprocess.run(command, capture_output=True)
    error_code = results.returncode
    if error_code != 0:
        error_message = results.stderr
        print(error_message)
        exit(error_code)


install_dev_dependencies("pip")
