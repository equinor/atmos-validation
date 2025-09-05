from random import randint
from typing import List, Tuple, Union

import xarray as xr

from ....schemas import (
    DIRECTION,
    FREQUENCY,
    HEIGHT_DIM_PREFIX,
    SOUTH_NORTH,
    TIME,
    WEST_EAST,
    ParameterConfig,
)
from ...utils import Severity, validation_node


@validation_node(severity=Severity.WARNING)
def sig_dig_validator(
    data: xr.DataArray, expected: ParameterConfig, number_of_iterations: int = 100
) -> List[str]:
    """
    Check if values have the correct minimum amount of significant decimals.
    This is checked by grabbing random indexes for "number_of_iterations" times.
    """
    results = []
    faults = 0

    for _ in range(number_of_iterations):
        random_index = _get_random_index(data)
        random_value = data[random_index]
        sig_digs = str(random_value.values)[::-1].find(".")
        if sig_digs == -1:
            # If there is no decimal separation it is most likely a fill value (nan)
            continue
        if sig_digs < expected.number_of_significant_decimals:
            faults += 1

    if faults > 0:
        results += [
            f"{faults}/{number_of_iterations} random samples had less than {expected.number_of_significant_decimals}"
            f"significant decimals for variable {data.name}"
        ]
    return results


def _get_random_index(data: xr.DataArray) -> Tuple[Union[int, slice], ...]:
    random_index = ()
    for dim in data.dims:
        if dim == TIME:
            random_index += (randint(0, len(data[TIME]) - 1),)
        elif dim == f"{HEIGHT_DIM_PREFIX}{data.name}":
            random_index += (
                randint(0, len(data[f"{HEIGHT_DIM_PREFIX}{data.name}"]) - 1),
            )
        elif dim == SOUTH_NORTH:
            random_index += (randint(0, len(data[SOUTH_NORTH]) - 1),)
        elif dim == WEST_EAST:
            random_index += (randint(0, len(data[WEST_EAST]) - 1),)
        elif dim == FREQUENCY:
            random_index += (randint(0, len(data[FREQUENCY]) - 1),)
        elif dim == DIRECTION:
            random_index += (randint(0, len(data[DIRECTION]) - 1),)
        else:
            raise ValueError(
                f"Invalid dimension {dim}, cannot validate interval of {data.name}"
            )
    return random_index
