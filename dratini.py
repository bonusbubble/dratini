#!/usr/bin/env python3

from ast import parse as _parse_python
from dratini.code_generation.cpp import generate_cpp
from dratini.utils import load_text_files_as_one, parse_program_arguments, print_dump, save_text_file, throw_feature_not_supported
import os
from random import randint
import subprocess
from tempfile import TemporaryDirectory


__dir__ = os.path.dirname(os.path.abspath(__file__))

LINKING_DIR = os.path.join(__dir__, "dratini", "linking")
INCLUDE_DIR = os.path.join(LINKING_DIR, "include")
LIB_DIR = os.path.join(LINKING_DIR, "lib")


def _add_dratini_flags_to_cxx_command(command: list[str]) -> list[str]:
    command.append("-std=c++17")
    command.append("-I" + INCLUDE_DIR)
    command.append("-L" + LIB_DIR)
    command.append("-l:libbgc.a")
    command.append("-l:libraylib.a")
    return command


def cxx(
        cxx: str="clang++",
        input_source_code: str=None,
        input_path: str=None,
        output_path: str=None,
        output_format: str="elf"
):
    result = None
    with TemporaryDirectory() as tmp_dir_obj:
        tmp_dir = str(tmp_dir_obj)
        command = [ cxx ]
        if input_path is None:
            file_id = randint(0x00000000, 0xFFFFFFFF)
            input_path = os.path.join(tmp_dir, str(file_id) + ".cpp")
            save_text_file(input_path, input_source_code)
        command.append(input_path)
        if output_path is not None and len(output_path) > 0:
            command.append("-o")
            command.append(output_path)
        else:
            command.append("-xc++")
            command.append("-")
        command = _add_dratini_flags_to_cxx_command(command)
        # print(" ".join(command))
        # exit()
        result = subprocess.run(command)
    return result


# Parse the arguments passed to the program.
args = parse_program_arguments()

# Get the source code to parse.
python_source_code = load_text_files_as_one(args.input)

# Parse the source code into an AST.
python_module = _parse_python(python_source_code)

# If the program should print the AST:
if args.ast:
    # Print the AST.
    print_dump(python_module)
    # Exit the program.
    exit()

# Generate C++ source code from the Python module.
cpp_source_code = generate_cpp(python_module)

# If the program should print the AST:
if args.emit_cpp:
    # If an output file was not specified:
    if args.output == None or len(args.output) < 1:
        # Write the C++ source code to the standard output stream (STDOUT).
        print(cpp_source_code)
    # Otherwise:
    else:
        # Write the C++ source code to the output file.
        save_text_file(args.output, cpp_source_code)
    # Exit the program.
    exit()

# Compile the generated C++ source code into machine code.
cxx(
        input_source_code=cpp_source_code,
        output_path=args.output,
        output_format=args.format
)
