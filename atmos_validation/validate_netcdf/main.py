"""
This library can be used both as a CLI and as a library
In both cases a path will be provided to the validate
function. The path should be to a folder containing one or more
netcdf files which all belong to the same dataset or to a single netcdf file. The datafiles
should be compatible with xarray.open_mfdataset

To use as library:
from atmos_validation.main import validate.
validate(path_to_dataset_directory) or validate(path_to_dataset_file)

To use as CLI, see docstring.
"""

import logging
import sys
from pprint import pprint
from typing import List, Optional

import xarray as xr

from . import validation_settings
from .external_reference_guard import (
    ExternalReferenceError,
    assert_no_external_references,
)
from .utils import get_file_paths_in_folder
from .validation_logger import log
from .validators.root_validator import ValidationResult, root_validator

DOCSTRING = f"""
Usage: python -m atmos_toolkit validate-dataset DIR_OR_FILE [OPTIONS]

Example: python -m atmos_toolkit validate-dataset my_dataset/ {validation_settings.RANDOM_SEED} 42

Run validation on a hindcast or measurement dataset (NetCDF standard format check)

Args:
    DIR_OR_FILE \t \t The directory containing hindcast or the single .nc file to be validated

Options:
    --{validation_settings.CHECK_MIN_MAX_FULL} \t\t Verify min/max values for entire dataset. 
    \t\t\t\t\t Can be extremely slow for large datasets. Default behaviour is taking random samples.
    --{validation_settings.SKIP_MIN_MAX_CHECK} \t Skip random sample check for min/max values.
    --{validation_settings.SKIP_WARNINGS} \t\t\t Skip all checks that would only output a "WARNING".
    --{validation_settings.RANDOM_SEED} <int> \t Fix the random seed so sampled checks are reproducible.
"""


def main():
    log.create_or_update_logger()
    log.info(sys.argv)
    if len(sys.argv) <= 2:
        print(DOCSTRING)
        sys.exit(2)

    try:
        result = validate(sys.argv[2], additional_args=sys.argv[2:])
    except Exception as e:
        log.error(e)
        print(f"Validation failed with an unexpected error: {e!r}")
        sys.exit(1)

    log.info("Validation finished")
    if result.errors:
        pretty_print_result(
            result.errors,
            description=f"Found {len(result.errors)} errors. These must be fixed:",
        )
    if result.warnings:
        pretty_print_result(
            result.warnings,
            description=f"Found {len(result.warnings)} warnings. These are FYI and can be ignored:",
        )
    if not result.warnings + result.errors:
        print("Looks good! File validated with 0 errors and 0 warnings")

    if result.errors:
        sys.exit(1)


def validate(
    path: str,
    injected_logger: Optional[logging.Logger] = None,
    additional_args: Optional[List[str]] = None,
) -> ValidationResult:
    """
    Execute validation on a directory or file.

    Args:
        path: path to a folder of datasets which can be collated in
        a mfdataset. The folder must not contain any other *.nc files
        than the ones included in the set under validation
        injected_logger: pass a logger to be used for validation
        additional_args: see docstring "Options" for available additional_args.

    Returns:
        ValidationResult containing errors and warning from running validation
    """
    log.create_or_update_logger(injected_logger)
    validation_settings.apply_settings(additional_args or [])

    try:
        log.info("load dataset from path %s", path)
        paths = load_paths(path)
        if not paths:
            raise OSError("No NetCDF files in dir")
    except Exception as err:
        return ValidationResult(
            errors=[f"file:Could not open files in path {path}", repr(err)],
            warnings=[],
        )

    ds = None
    try:
        assert_no_external_references(paths)
        ds = open_mf_dataset(paths)
        result = root_validator(ds, paths)
        return ValidationResult(
            warnings=list(set(result.warnings)),
            errors=result.errors,
        )
    except ExternalReferenceError as err:
        return ValidationResult(errors=[f"file:{err}"], warnings=[])
    except Exception as err:
        return ValidationResult(errors=[repr(err)], warnings=[])
    finally:
        if ds:
            ds.close()


def load_paths(path: str) -> List[str]:
    """
    Parameters
    ----------
    path: A path to a folder of datasets which can be collated in
    a mfdataset. The folder must not contain any other *.nc files
    than the ones included in the set under validation
    """
    if path.endswith(".nc"):
        return [path]
    return get_file_paths_in_folder(path)


def open_mf_dataset(paths: List[str]) -> xr.Dataset:
    xr.set_options(use_new_combine_kwarg_defaults=True)
    if len(paths) > 1:
        log.info("Running open mfdataset for %s files", len(paths))
        try:
            ds = xr.open_mfdataset(
                paths,
                engine="h5netcdf",
                concat_dim="Time",
                compat="equals",
                data_vars="minimal",
                combine="nested",
                combine_attrs="override",
                chunks="auto",
                parallel=True,
            )
        except xr.MergeError as err:
            # Static coords (LAT/LON/height) must be identical across a dataset;
            # compat="equals" surfaces mismatches that would otherwise be dropped.
            raise ValueError(
                "Conflicting static coordinates between files in the dataset. "
                "All files in a dataset must share the same grid "
                f"(LAT/LON/height). Details: {err}"
            ) from err
    else:
        log.info("Running open dataset for single file %s", paths[0])
        ds = xr.open_dataset(paths[0], engine="h5netcdf")
    return ds


def pretty_print_result(results: List[str], description: str, width: int = 150):
    print("-" * width)
    print(description)
    print("-" * width)
    pprint(results, width=width, indent=4)
