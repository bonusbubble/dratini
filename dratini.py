#!/usr/bin/env python3

import argparse
from ast import parse as _parse_python
from dratini.code_generation.cpp import generate_cpp as _generate_cpp
from dratini.utils import load_text_files_as_one as _load_text_files_as_one, parse_program_arguments as _parse_program_arguments, platform_tag as _platform_tag, print_dump as _print_dump, save_text_file as _save_text_file, throw_feature_not_supported as _throw_feature_not_supported
import os
from random import randint
import subprocess
from tempfile import TemporaryDirectory


# Get the path to this script.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LINKING_DIR = os.path.join(_SCRIPT_DIR, "dratini", "linking")
_INCLUDE_DIR = os.path.join(_LINKING_DIR, "include")
_LIB_DIR = os.path.join(_LINKING_DIR, "lib")


def _lib_dir() -> str:
    return _LIB_DIR


def _add_dratini_base_flags_to_cxx_command(command: list[str], args: argparse.Namespace) -> list[str]:
    command.append("-std=c++17")
    command.append("-I" + _INCLUDE_DIR)
    if not args.emit_asm and not args.emit_obj:
        command.append("-L" + _LIB_DIR)
        command.append("-l:libbgc.a")
        command.append("-l:libraylib.a")
    return command


def _add_dratini_inherited_flags_to_cxx_command(command: list[str], args: argparse.Namespace) -> list[str]:
    if args.emit_asm or args.emit_llvm:
        command.append("-S")
    if args.emit_bin:
        command.append("-Wl,--oformat=binary")
    if args.emit_llvm:
        command.append("-emit-llvm")
    if args.emit_obj:
        command.insert(0, "-c")
    return command


def _add_dratini_user_flags_to_cxx_command(command: list[str], args: argparse.Namespace) -> list[str]:
    cxxflags_str = args.cxxflags
    if "\"" in cxxflags_str:
        _throw_feature_not_supported("cxxflags_with_quotes")
    cxxflags = cxxflags_str.split(" ")
    for cxxflag in cxxflags:
        command.append(cxxflag)
    return command


def _get_cxx_flags(
        args: argparse.Namespace
) -> str:
    flags = []
    flags = _add_dratini_base_flags_to_cxx_command(flags, args)
    flags = _add_dratini_inherited_flags_to_cxx_command(flags, args)
    flags = _add_dratini_user_flags_to_cxx_command(flags, args)
    return flags


def _cxx(
        input_source_code: str=None,
        input_path: str=None,
        output_path: str=None,
        args: argparse.Namespace = argparse.Namespace()
):
    result = None
    with TemporaryDirectory() as tmp_dir_obj:
        tmp_dir = str(tmp_dir_obj)
        command = []
        if input_path is None:
            file_id = round(abs(randint(0x00000000, 0xFFFFFFFF)))
            input_path = os.path.join(tmp_dir, str(file_id) + ".cpp")
            _save_text_file(input_path, input_source_code)
        command.append(input_path)
        if output_path is not None and len(output_path) > 0:
            command.append("-o")
            command.append(output_path)
        else:
            command.append("-xc++")
            command.append("-")
        cxx_flags = _get_cxx_flags(args)
        command.extend(cxx_flags)
        cxx = args.cxx
        command.insert(0, cxx)
        # print(" ".join(command))
        # exit()
        result = subprocess.run(command)
    return result


def _main(args: argparse.Namespace):
    # If the program should print the C++ compiler flags:
    if args.emit_cxxflags:
        cxx_flags = _get_cxx_flags(args)
        print(" ".join(cxx_flags))
        exit()

    if args.emit_target:
        platform_tag = _platform_tag(args.cxx)
        print(platform_tag)
        exit()

    # Get the source code to parse.
    python_source_code = _load_text_files_as_one(args.input)

    # Parse the source code into an AST.
    python_module = _parse_python(python_source_code)

    # If the program should print the AST:
    if args.emit_ast:
        # Print the AST.
        _print_dump(python_module)
        # Exit the program.
        exit()

    # Generate C++ source code from the Python module.
    cpp_source_code = _generate_cpp(python_module)

    # If the program should print the AST:
    if args.emit_cpp:
        # If an output file was not specified:
        if args.output == None or len(args.output) < 1:
            # Write the C++ source code to the standard output stream (STDOUT).
            print(cpp_source_code)
        # Otherwise:
        else:
            # Write the C++ source code to the output file.
            _save_text_file(args.output, cpp_source_code)
        # Exit the program.
        exit()

    # Compile the generated C++ source code into machine code.
    _cxx(
            input_source_code=cpp_source_code,
            output_path=args.output,
            args=args
    )


if __name__ == "__main__":
    # Parse the arguments passed to the program.
    args = _parse_program_arguments()

    # If a C++ compiler was provided:
    if args.cxx != "clang++" and args.target == _platform_tag():
        args.target = _platform_tag(args.cxx)

    _LIB_DIR = os.path.join(_lib_dir(), args.target)

    _main(args)
