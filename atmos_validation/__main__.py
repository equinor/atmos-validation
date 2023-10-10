"""
This is the entry point for atmos_validation when run as a CLI.
"""

import sys

from .convert_ascii import main as convert_ascii
from .validate_ascii import main as validate_ascii
from .validate_netcdf import main as validate_netcdf

DOCSTRING = """
Usage: python -m atmos_validation COMMAND [ARGS] [OPTIONS]
    
Metocean-data validation-tools for the Equinor-Atmos project.

Commands:
    validate-netcdf \t \t Run validation on a hindcast or measurement dataset (NetCDF standard format check)
    validate-ascii \t \t Run validation on a measurement ascii file
    convert-ascii \t \t Convert a measurement ascii file to NetCDF standard
"""


def main():
    try:
        if sys.argv[1] == "validate-netcdf":
            validate_netcdf()
        elif sys.argv[1] == "validate-ascii":
            validate_ascii()
        elif sys.argv[1] == "convert-ascii":
            convert_ascii()
        else:
            print(DOCSTRING)

    except IndexError:
        print(DOCSTRING)

    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
