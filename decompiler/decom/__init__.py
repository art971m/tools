import argparse
import pathlib
import sys
from enum import Enum
from os import linesep

from . import exceptions


def main():
    try:
        args = _parse_args()
    except exceptions.CommandLineOptions as error:
        sys.stderr.write(str(error) + linesep)
        sys.stderr.write(error.parser.format_help())
        sys.exit(1)


class Options(Enum):
    INPUT_DIR = '--input-dir'
    OUTPUT_DIR = '--output-dir'
    JD_CLI = '--jd-cli'
    CLEAN_OUTPUT_DIR = '--clean-output-dir'


def _parse_args():
    parser = argparse.ArgumentParser(
        description=(
            'The dc is a command line interface for the Java Decompiler. '
            'The application decompile *.jar files. '
            'Java runtime is required in version 8 or newer and jd-cli https://github.com/intoolswetrust/jd-cli'
        ),
    )

    parser.add_argument(Options.INPUT_DIR.value, dest=Options.INPUT_DIR.name, type=pathlib.Path,
                        help='Path to input directory', required=True)
    parser.add_argument(Options.OUTPUT_DIR.value, dest=Options.OUTPUT_DIR.name, type=pathlib.Path,
                        help='Path to output directory', required=True)
    parser.add_argument(Options.JD_CLI.value, dest=Options.JD_CLI.name, type=pathlib.Path,
                        help='Path to jd-cli', required=True)
    parser.add_argument(Options.CLEAN_OUTPUT_DIR.value, dest=Options.CLEAN_OUTPUT_DIR.name, action='store_true',
                        help='Cleans the output directory before decompilation',
                        required=False, default=False)

    args = parser.parse_args()

    for option in [Options.INPUT_DIR, Options.OUTPUT_DIR]:
        path = vars(args)[option.name]
        if not path.exists():
            raise exceptions.CommandLineOptions(f"Directory {option.value} '{str(path)}' does not exist", parser)
        if not path.is_dir():
            raise exceptions.CommandLineOptions(f"Option {option.value} '{str(path)}' is not a directory", parser)

    path = vars(args)[Options.JD_CLI.name]
    if not path.exists():
        raise exceptions.CommandLineOptions(f"jd-cli '{str(path)}' does not exist", parser)

    return args
