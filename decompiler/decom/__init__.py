import argparse
import pathlib


def main():
    args = _parse_args()


def _parse_args():
    parser = argparse.ArgumentParser(
        description=(
            'The dc is a command line interface for the Java Decompiler. '
            'The application decompile *.jar files. '
            'Java runtime is required in version 8 or newer and jd-cli https://github.com/intoolswetrust/jd-cli'
        ),
    )

    parser.add_argument('--input-dir', type=pathlib.Path, help='Path to input directory', required=True)
    parser.add_argument('--output-dir', type=pathlib.Path, help='Path to output directory', required=True)
    parser.add_argument('--jd-cli', type=pathlib.Path, help='Path to jd-cli', required=True)
    parser.add_argument('--clean-output-dir', action='store_true',
                        help='Cleans the output directory before decompilation',
                        required=False, default=False)

    return parser.parse_args()
