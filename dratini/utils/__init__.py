import argparse as _argparse
from ast import dump as _dump_python_ast
import subprocess

from dratini.projectconfig import *

from .hex2 import hex2
from .error_handling import *


def _get_default_output(
        format: str
) -> str:
    # Windows Executable
    if format == "exe":
        return "program.exe"
    # C++
    if format == "cpp":
        return "main.cpp"
    # Default
    return "program"


def list_bool(
        values: list[object]
) -> list[bool]:
    converted_values = []
    for value in values:
        converted_value = bool(value)
        converted_values.append(converted_value)
    return converted_values


def list_int(
        values: list[object]
) -> list[int]:
    converted_values = []
    for value in values:
        converted_value = int(value)
        converted_values.append(converted_value)
    return converted_values


def list_float(
        values: list[object]
) -> list[float]:
    converted_values = []
    for value in values:
        converted_value = float(value)
        converted_values.append(converted_value)
    return converted_values


def list_str(
        values: list[object]
) -> list[str]:
    converted_values = []
    for value in values:
        converted_value = str(value)
        converted_values.append(converted_value)
    return converted_values


def platform_tag(cxx: str="clang++") -> str:
    command = [cxx, "-dumpmachine"]
    completed_process = subprocess.run(command, capture_output=True)
    error_message = completed_process.stderr
    if error_message:
        print(error_message)
        exit(1)
    output = completed_process.stdout.decode("utf-8").strip()
    return output


def print_dump(
        object_: object
) -> str:
    # Get a prettified dump of the AST.
    python_ast_dump = _dump_python_ast(object_, indent=4)
    # Print the dump.
    print(python_ast_dump)


def resolve_variable_name(
        function_id: int,
        variable_name: str
) -> str:
    # If the variable name is an unmangled variable name:
    if "__" in variable_name:
        # Return the resolved unmangled variable name.
        return resolve_unmangled_variable_name(variable_name)
    # Return the resolved local variable name.
    return resolve_local_variable_name(function_id, variable_name)


def is_linux() -> bool:
    return _PLATFORM.name == "Linux"


def is_windows() -> bool:
    return _PLATFORM.name == "Windows"


def resolve_local_variable_name(
        function_id: int,
        variable_name: str
) -> str:
    function_id_hex = _resolve_hex(function_id)
    variable_name_hex = _resolve_hex(variable_name)
    resolved_variable_name = "_" + function_id_hex + "_" + variable_name_hex
    return resolved_variable_name


def resolve_unmangled_variable_name(
        variable_name: str
) -> str:
    return variable_name


def load_text_file(
        file_path: str
) -> str:
    '''
    Load the contents of a text file.
    '''
    # Open the file and close the resource afterwards.
    with open(file_path, 'r') as file:
        # Read and return the contents of the file.
        return file.read().strip()


def load_text_files(
        input_paths: list[str]
) -> list[str]:
    '''
    Load the contents of multiple text files.
    '''
    # Create an empty list to hold the contents of each file.
    file_contents = []
    # For each file path:
    for file_path in input_paths:
        # Load the contents of the text file.
        file_content = load_text_file(file_path)
        # Add the contents of the text file to the list.
        file_contents.append(file_content)
    # Return the list of contents of each file.
    return file_contents


def load_text_files_as_one(
        input_paths: list[str]
) -> str:
    '''
    Load the contents of multiple text files as one string.
    '''
    file_contents = load_text_files(input_paths)
    return "\n".join(file_contents)


def parse_program_arguments() -> object:
    '''
    Parse any arguments passed to the program.
    '''
    # Create a new program argument parser.
    argument_parser = _argparse.ArgumentParser(
            prog = "dratini",
            description = "dratini " + PROJECT.version_tag + " - Dratini AOT Compiler",
            epilog = PROJECT.copyright,
            usage = "dratini <input+> [options] -o <output>"
    )
    # Add arguments to the parser.
    argument_parser.add_argument(
            "input",
            action="extend",
            nargs="*",
            type=str,
            help="one or more input files to read"
    )
    argument_parser.add_argument(
            "--cxx",
            type = str,
            default = "clang++",
            help="path to C++ compiler",
            metavar="cxx"
    )
    argument_parser.add_argument(
            "--cxxflags",
            type = str,
            default = "",
            help="C++ compiler flags",
            metavar="flags"
    )
    argument_parser.add_argument(
            "--debug",
            action="store_true",
            help="enable debugging mode"
    )
    argument_parser.add_argument(
            "--emit-asm",
            action="store_true",
            help="emit assembly code"
    )
    argument_parser.add_argument(
            "--emit-ast",
            action="store_true",
            help="emit an AST (Abstract Syntax Tree)"
    )
    argument_parser.add_argument(
            "--emit-bin",
            action="store_true",
            help="emit raw binary machine code"
    )
    argument_parser.add_argument(
            "--emit-cpp",
            action="store_true",
            help="emit C++ source code"
    )
    argument_parser.add_argument(
            "--emit-cxxflags",
            action="store_true",
            help="emit the list of flags needed to pass to the C++ compiler to compile the Dratini source code"
    )
    argument_parser.add_argument(
            "--emit-llvm",
            action="store_true",
            help="emit LLVM IR code"
    )
    argument_parser.add_argument(
            "-c",
            "--emit-obj",
            action="store_true",
            help="emit object code"
    )
    argument_parser.add_argument(
            "--emit-target",
            action="store_true",
            help="emit target platform tag"
    )
    argument_parser.add_argument(
            "-o",
            "--output",
            type = str,
            default = "",
            help="write the output to file",
            metavar="path"
    )
    argument_parser.add_argument(
            "-T",
            "--target",
            type = str,
            default = platform_tag(),
            help="write the output to file",
            metavar="path"
    )
    version_message = "%(prog)s " + PROJECT.version_tag + " [" + platform_tag() + "]" + " - " + PROJECT.copyright
    argument_parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=version_message
    )
    argument_parser.add_argument(
            "-V",
            "--verbose",
            action="store_true",
            help="enable verbose mode"
    )
    # Parse the program arguments.
    program_arguments = argument_parser.parse_args()
    # Auto-detect the output format using the output file extension.
    # Get the file extension of the output file path.
    output_file_extension = program_arguments.output.split(".")[-1]
    # Use the output file extension as the default output format.
    if not program_arguments.emit_asm and not program_arguments.emit_ast and not program_arguments.emit_bin and not program_arguments.emit_cpp and not program_arguments.emit_llvm:
        if output_file_extension == "s" or output_file_extension == "asm":
            program_arguments.emit_asm = True
        if output_file_extension == "ast":
            program_arguments.emit_ast = True
        if output_file_extension == "bin":
            program_arguments.emit_bin = True
        if output_file_extension == "cpp" or output_file_extension == "cc":
            program_arguments.emit_cpp = True
        if output_file_extension == "ll":
            program_arguments.emit_llvm = True
    # Return the program's arguments.
    return program_arguments


def save_text_file(
        path: str,
        data: str
):
    '''
    Save the contents of a text file.
    '''
    # Open the file and close the resource afterwards.
    with open(path, 'w') as file:
        # Write the contents of the file.
        return file.write(data)


def _resolve_hex(
        value: object
) -> str:
    hash_code = value
    if isinstance(hash_code, int):
        hash_code = 11 * hash_code * 13 * hash_code * 27
    hash_code = hash(hash_code)
    return hex2(hash_code)[:6]
