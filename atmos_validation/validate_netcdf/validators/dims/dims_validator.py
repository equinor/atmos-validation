from typing import List

import xarray as xr

from ...utils import Severity, validation_node
from .dimvars_validator import dimvars_validator
from .spatial_validators import (
    lat_lon_validator,
    south_north_validator,
    west_east_validator,
)
from .time_validator import time_validator


@validation_node(severity=Severity.ERROR)
def dims_validator(ds: xr.Dataset, paths: List[str]) -> List[str]:
    return (
        time_validator(ds, paths)
        + dimvars_validator(ds)
        + south_north_validator(ds)
        + west_east_validator(ds)
        + lat_lon_validator(ds)
    )
