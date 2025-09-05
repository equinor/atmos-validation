"""
Dimensions on each data variable is checked against
parameters.json in the vardims_validator
"""

from typing import List

import xarray as xr

from ....schemas import SOUTH_NORTH, WEST_EAST
from ...utils import Severity, validation_node

REQUIRED_LAT_ATTRS = {
    "short_name": "Latitude",
    "long_name": "Latitude",
    "CF_standard_name": "latitude",
    "description": "Latitude",
    "units": "degree_north",
}

REQUIRED_LON_ATTRS = {
    "short_name": "Longitude",
    "long_name": "Longitude",
    "CF_standard_name": "longitude",
    "description": "Longitude",
    "units": "degree_east",
}

REQUIREDS_MAP = {"LAT": REQUIRED_LAT_ATTRS, "LON": REQUIRED_LON_ATTRS}


@validation_node(severity=Severity.ERROR)
def existence_validator(ds: xr.Dataset, dim_name: str) -> List[str]:
    result = []
    if dim_name not in list(ds.dims):
        result += [f"{dim_name} is not a dimension in dataset"]
    elif len(ds[dim_name]) == 0:
        result += [f"{dim_name} has length 0"]
    return result


@validation_node(severity=Severity.ERROR)
def lat_lon_validator(ds: xr.Dataset) -> List[str]:
    result = []
    lats = ds["LAT"]
    lons = ds["LON"]
    expected_dims = [SOUTH_NORTH, WEST_EAST]
    if len(lats.shape) != len(expected_dims):
        result += [
            f"LAT has shape {lats.shape}. lats should be 2d, south_north and west_east"
        ]
    if len(lons.shape) != len(expected_dims):
        result += [
            f"LON has shape {lons.shape}. lons should be 2d, south_north and west_east"
        ]

    if list(lats.dims) != expected_dims:
        result += [f"dims for LAT should be {expected_dims}, found {lats.dims}"]
    if list(lons.dims) != expected_dims:
        result += [f"dims for LON should be {expected_dims}, found {lons.dims}"]

    return result + mandatory_attrs_lat_lon_validator(ds)


@validation_node(severity=Severity.ERROR)
def mandatory_attrs_lat_lon_validator(ds: xr.Dataset) -> List[str]:
    """
    Validates that LAT and LON have expected attrs and values
    given by the REQUIRED_MAP entries.
    """
    result = []
    for data_array in [ds["LAT"], ds["LON"]]:
        requireds = REQUIREDS_MAP[str(data_array.name)]
        for req_attr in requireds:
            try:
                req_value = requireds[req_attr]
                if req_attr not in data_array.attrs:
                    result += [f"{data_array.name} is missing attribute {req_attr}"]
                actual_value = data_array.attrs[req_attr]
                if req_value != actual_value:
                    result += [
                        f"Wrong attribute for {data_array.name} {req_attr}. "
                        f"Value was: {actual_value}, expected: {req_value}"
                    ]
            except Exception:
                continue  # skipping here to not double report any errors
    return result


@validation_node(severity=Severity.ERROR)
def south_north_validator(ds: xr.Dataset):
    """Validate that the dataset has south_north as a dim with a length > 0"""
    return existence_validator(ds, SOUTH_NORTH)


@validation_node(severity=Severity.ERROR)
def west_east_validator(ds: xr.Dataset):
    """Validate that the dataset has west_east as a dim with a length > 0"""
    return existence_validator(ds, WEST_EAST)
