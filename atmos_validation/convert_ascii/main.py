import sys

from .df_to_nc import ascii_to_nc

DOCSTRING = """
Usage: python -m atmos_validation convert-ascii [SRC_FILENAME]

Convert a .dat, .txt or .LIS file to Atmos compliant NetCDF file.

Args:
    SRC_FILENAME \t \t The source file in .dat, .txt or .LIS format to convert
"""


def main():
    try:
        src_filename = sys.argv[2]
        ascii_to_nc(src_filename)

    except IndexError:
        print(DOCSTRING)
