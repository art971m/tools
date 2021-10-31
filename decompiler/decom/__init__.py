import argparse
import pathlib
import shutil
import subprocess
import sys
from enum import Enum
from os import linesep

from . import exceptions


class Options(Enum):
    INPUT_DIR = '--input-dir'
    OUTPUT_DIR = '--output-dir'
    JD_CLI = '--jd-cli'
    CLEAN_OUTPUT_DIR = '--clean-output-dir'


def main():
    try:
        args = _parse_args()
        if getattr(args, Options.CLEAN_OUTPUT_DIR.name):
            _clean(getattr(args, Options.OUTPUT_DIR.name))

        input_dir = getattr(args, Options.INPUT_DIR.name)
        for path in input_dir.rglob('*.jar'):
            if path.is_symlink() or path.is_dir():
                pass
            else:
                _decompile_jar(path, args)
    except exceptions.CommandLineOptions as error:
        sys.stderr.write(str(error) + linesep)
        sys.stderr.write(error.parser.format_help())
        sys.exit(1)


def _clean(dir):
    if dir.is_dir():
        for path in dir.iterdir():
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink()
    else:
        dir.unlink()


def _decompile_jar(path: pathlib.Path, args):
    output_dir = getattr(args, Options.OUTPUT_DIR.name)
    cmd = [
        str(getattr(args, Options.JD_CLI.name)),
        '--skipResources',
        '--outputDirStructured', str(output_dir),
        str(path)
    ]

    proc = subprocess.run(cmd)
    # proc.check_returncode()

    decompiled_dir = output_dir.joinpath(path.name)
    if decompiled_dir.exists():
        for decom_file in decompiled_dir.iterdir():
            target = output_dir.joinpath(decom_file.name)
            if decom_file.is_dir():
                shutil.copytree(decom_file, target, dirs_exist_ok=True)
            else:
                shutil.copy(decom_file, target)
        _clean(decompiled_dir)
        decompiled_dir.rmdir()


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
