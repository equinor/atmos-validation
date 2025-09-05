import re
from typing import List, cast

import numpy as np
import numpy.typing as npt
import xarray as xr
from h5py import Dataset, File

from ....schemas import TIME
from ...utils import Severity, convert_utc_timestamp_to_filename_format, validation_node


@validation_node(severity=Severity.ERROR)
def time_validator(ds: xr.Dataset, paths: List[str]) -> List[str]:
    result: List[str] = []
    time = ds.variables[TIME].data
    if not np.all(time[:-1] <= time[1:]):  # type: ignore
        result += ["Some timestamps in the dataset are not in sorted order"]

    result += filename_validator(paths)
    result += unique_validator(time)
    result += cf_standard_time_validator(ds)
    return result


@validation_node(severity=Severity.ERROR)
def filename_validator(paths: List[str]) -> List[str]:
    """Validates that filenames are named such that they can be sorted
    in a chronological order according to time axis, that all files
    contains entries in the time dimension and that the unit is matching
    the standard format

    Args:
        paths: list of str paths to the netcdf files to be validated

    Returns:
        list of error/warning messages to be printed as validation output
    """
    result = []
    start_times = []
    for path in sorted(paths):
        with File(path) as file:
            time_ds = cast(Dataset, file[TIME])
            time: npt.NDArray[np.int64] = time_ds[:]
            start_times.append(time[0])
            result += has_entries_validator(path, time)
            result += time_units_validator(path, time_ds)
    if not np.all(start_times[:-1] <= start_times[1:]):
        result = [
            "Filenames are not sortable such that time axis appears in increasing order"
        ]
    if len(paths) > 1:
        result += filename_convention_validator(paths)
        result += filename_includes_time_axis_validator(paths)
    return result


@validation_node(severity=Severity.WARNING)
def filename_convention_validator(paths: List[str]) -> List[str]:
    """Validates that files are named with a timestamp to provide
    readability and overview in the data lake. Only writes general
    warning for the whole directory, which is by design to not
    clutter the validation output (Consider dataset consisting of
    500 files all non-passing)

    Args:
        path: path that should include timestamps to be validated against dataset

    Returns:
        list of error/warning messages to be printed as validation output
    """
    result = []
    convention_checks = []
    for path in sorted(paths):
        check = convention_check(path)
        convention_checks.append(check)
    if not np.all(convention_checks):
        result += [
            "All should follow the preferred naming convention:"
            "'<name>_<start_date>_<end_date>_T<time_length>.nc' where date format "
            "follows 'YYYYMMDD'"
        ]
    return result


def convention_check(path: str) -> bool:
    """Validates that file is named with a timestamp to provide
    readability and overview in the data lake.

    Args:
        path: path that should include timestamps to be validated against dataset
        time_ds: dataset holding the actual timestamps

    Returns:
        A boolean indicator showing if validation passed or not
    """
    try:
        with File(path) as file:
            time_ds = cast(Dataset, file[TIME])
            expected_start, expected_end = re.findall(r"\d{8}", path.replace(".nc", ""))
            start = convert_utc_timestamp_to_filename_format(time_ds[0])
            end = convert_utc_timestamp_to_filename_format(time_ds[-1])
            return expected_start == start and expected_end == end
    except Exception:
        return False


@validation_node(severity=Severity.ERROR)
def filename_includes_time_axis_validator(paths: List[str]) -> List[str]:
    """Validates that files are named with a the length of the time
    axis (for ingestion arguments generation). Only writes general
    error for the whole directory, which is by design to not
    clutter the validation output (Consider dataset consisting of
    500 files all non-passing)

    Args:
        path: path that should include "T<len(time)> to be validated against dataset

    Returns:
        list of error/warning messages to be printed as validation output
    """
    result = []
    failed_checks = []
    for path in sorted(paths):
        try:
            ds = xr.open_dataset(path, engine="h5netcdf")
            length = int(path.removesuffix(".nc").split("_T")[-1])
            if length != len(ds.Time):
                failed_checks.append(path)
        except Exception:
            failed_checks.append(path)
    if failed_checks:
        result += [
            "All filenames MUST include the length of the time axis of the file as the last "
            "part of the file_name, e.g. '..._T<time_length>.nc'. Either this was missing or there "
            f"was a missmatch in time_axis length for the file names: {failed_checks}"
        ]
    return result


@validation_node(severity=Severity.ERROR)
def time_units_validator(path: str, time_ds: Dataset) -> List[str]:
    expected = b"microseconds since 1900-01-01"
    alt_expected = "microseconds since 1900-01-01"
    actual = time_ds.attrs["units"]
    if actual not in (expected, alt_expected):  # type: ignore
        return [
            f"time units attribute should be {expected}, found {actual} in file {path}"
        ]
    return []


@validation_node(severity=Severity.ERROR)
def has_entries_validator(path: str, times: npt.NDArray[np.int64]):
    "Checks that the time array is not empty"
    if len(times) == 0:
        return [f"File with path {path} has no entries in time dimension"]
    return []


@validation_node(severity=Severity.ERROR)
def unique_validator(time: npt.NDArray[np.datetime64]) -> List[str]:
    """Validate that there are no duplicate timestamps"""
    uniques, counts = np.unique(time, return_counts=True)
    duplicates = uniques[counts > 1]
    if len(duplicates) > 0:
        return [
            f"Duplicates found in Time dimension. Sample timestamps: {duplicates[0:3]}"
        ]
    return []


@validation_node(severity=Severity.ERROR)
def cf_standard_time_validator(ds: xr.Dataset) -> List[str]:
    result = []
    try:
        cf_standard = ds[TIME].attrs["CF_standard_name"]
        if cf_standard != "time":
            result += [
                f"""CF_standard name for {TIME} should be "time". Found: {cf_standard}"""
            ]
    except KeyError:
        result += [f"{TIME} is missing attribute CF_standard_name"]
    return result
