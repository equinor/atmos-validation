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
from .utils import get_file_paths_in_folder
from .validation_logger import log
from .validators.root_validator import ValidationResult, root_validator

DOCSTRING = f"""
Usage: python -m atmos_toolkit validate-dataset DIR_OR_FILE

Run validation on a hindcast or measurement dataset (NetCDF standard format check)

Args:
    DIR_OR_FILE \t \t The directory containing hindcast or the single .nc file to be validated

Options:
    --{validation_settings.CHECK_MIN_MAX_FULL} \t\t Verify min/max values for entire dataset. 
    \t\t\t\t\t Can be extremely slow for large datasets. Default behaviour is taking random samples.
    --{validation_settings.SKIP_MIN_MAX_CHECK} \t Skip random sample check for min/max values.
    --{validation_settings.SKIP_WARNINGS} \t\t\t Skip all checks that would only output a "WARNING".
    --{validation_settings.BATCH_SIZE} \t\t\t Set the amount of .nc files per batch to validate. Defaults to 1000.
"""


def main():
    log.create_or_update_logger()
    log.info(sys.argv)
    try:
        if len(sys.argv) <= 2:
            print(DOCSTRING)
        else:
            result = validate(sys.argv[2], additional_args=sys.argv[2:])
            if isinstance(result, ValidationResult):
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
    except Exception as e:
        log.error(e)
        print(DOCSTRING)


def validate(
    path: str,
    injected_logger: Optional[logging.Logger] = None,
    additional_args: Optional[List[str]] = None,
    batch_size: Optional[int] = None,
) -> ValidationResult:
    """
    Execute validation on a directory or file.

    Args:
        path: path to a folder of datasets which can be collated in
        a mfdataset. The folder must not contain any other *.nc files
        than the ones included in the set under validation
        injected_logger: pass a logger to be used for validation
        additional_args: see docstring "Options" for available additional_args.
        batch_size: Since open_mfdataset is slow for opening large amount of files,
        validation can be run in batches. Defaults to 1000 files per open_mfdataset/batch.

    Returns:
        ValidationResult containing errors and warning from running validation
    """
    log.create_or_update_logger(injected_logger)
    if additional_args:
        validation_settings.apply_settings(additional_args)
    if batch_size:
        validation_settings.set_batch_size(override=batch_size)

    try:
        log.info("load dataset from path %s", path)
        batches = load_paths(path, batch_size=validation_settings.get_batch_size())
        validation_settings.NO_OF_BATCHES = len(batches)
        if not batches:
            raise OSError("No NetCDF files in dir")
    except Exception as err:
        return ValidationResult(
            errors=[f"file:Could not open files in path {path}", repr(err)],
            warnings=[],
        )

    ds = None
    try:
        warnings = []
        for i, batch in enumerate(batches):
            print(f"validating batch: {i+1} of {len(batches)}")
            ds = open_mf_dataset(batch)
            batch_result = root_validator(ds, batch)
            warnings += batch_result.warnings
            if batch_result.errors:  # early exit if error occurs in batch
                return ValidationResult(
                    warnings=list(set(warnings)),
                    errors=batch_result.errors,
                )
        return ValidationResult(warnings=list(set(warnings)), errors=[])
    except Exception as err:
        return ValidationResult(errors=[repr(err)], warnings=[])
    finally:
        if ds:
            ds.close()


def load_paths(path: str, batch_size: int) -> List[List[str]]:
    """
    Parameters
    ----------
    path: A path to a folder of datasets which can be collated in
    a mfdataset. The folder must not contain any other *.nc files
    than the ones included in the set under validation
    """
    if path.endswith(".nc"):
        paths = [path]
    else:
        paths = get_file_paths_in_folder(path)
    batches = []
    for i in range(0, len(paths), batch_size):
        batch = paths[i : i + batch_size]
        batches.append(batch)
    return batches


def open_mf_dataset(paths: List[str]) -> xr.Dataset:
    xr.set_options(use_new_combine_kwarg_defaults=True)
    if len(paths) > 1:
        log.info("Running open mfdataset for %s files", len(paths))
        ds = xr.open_mfdataset(
            paths,
            engine="h5netcdf",
            concat_dim="Time",
            compat="override",
            data_vars="minimal",
            combine="nested",
            chunks="auto",
            parallel=True,
        )
    else:
        log.info("Running open dataset for single file %s", paths[0])
        ds = xr.open_dataset(paths[0], engine="h5netcdf")
    return ds


def pretty_print_result(results: List[str], description: str, width: int = 150):
    print("-" * width)
    print(description)
    print("-" * width)
    pprint(results, width=width, indent=4)
