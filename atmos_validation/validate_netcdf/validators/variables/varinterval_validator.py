import random
import sys
from typing import List, Tuple, Union

import xarray as xr

from ....schemas import (
    DIRECTION,
    FREQUENCY,
    SOUTH_NORTH,
    TIME,
    WEST_EAST,
    ParameterConfig,
    get_acceptable_dims_from_parameter_key,
    get_height_dim_from_parameter_key,
)
from ... import validation_settings
from ...utils import Severity, validation_node
from ...validation_logger import log

SEED = random.randrange(sys.maxsize)
print(f"using random seed: {SEED}")


def _get_random_time_slice(actual: xr.DataArray, rand: random.Random) -> slice:
    """To save processing time we only check 5000 timestamps random samples"""
    len_time = len(actual.Time)
    sample_size = 5000 // validation_settings.NO_OF_BATCHES
    if len_time > sample_size * 2:
        start = rand.randint(0, len_time - sample_size - 1)
        time_slice = slice(
            start,
            start + sample_size,
        )
    else:
        start = rand.randint(0, len_time // 2)
        time_slice = slice(
            start,
            start + len_time // 2,
        )
    return time_slice


def _get_slice_tuple(
    dims: List[str], actual: xr.DataArray, rand: random.Random
) -> Tuple[Union[int, slice], ...]:
    result: Tuple[Union[int, slice], ...] = ()
    key = str(actual.name)
    height_dim = get_height_dim_from_parameter_key(key)
    for dim in dims:
        if dim == TIME:
            result += (_get_random_time_slice(actual, rand),)
        elif dim == SOUTH_NORTH:
            result += (slice(None, None),)
        elif dim == WEST_EAST:
            result += (slice(None, None),)
        elif dim == height_dim:
            result += (slice(None, None),)
        elif dim == FREQUENCY:
            result += (slice(None, None),)
        elif dim == DIRECTION:
            result += (slice(None, None),)
        else:
            raise ValueError(
                f"Invalid dimension {dim}, cannot validate interval of {key}"
            )
    return result


@validation_node(severity=Severity.ERROR)
def none_less_than_min_validator(
    actual: xr.DataArray, expected: ParameterConfig
) -> List[str]:
    if expected.min == "NA":
        return []
    smallest = round(
        float(actual.min().load()), expected.number_of_significant_decimals
    )
    if smallest < expected.min:
        return [
            f"{actual.name} has a value lower than configured minimum: configured min:"
            f" {expected.min}. Actual min: {smallest}"
        ]
    return []


@validation_node(severity=Severity.ERROR)
def none_larger_than_max_validator(
    actual: xr.DataArray, expected: ParameterConfig
) -> List[str]:
    if expected.max == "NA":
        return []
    largest = round(float(actual.max().load()), expected.number_of_significant_decimals)
    if largest > expected.max:
        return [
            f"{actual.name} has a value higher than configured maximum: configured max:"
            f" {expected.max}. Actual max: {largest}"
        ]
    return []


@validation_node(severity=Severity.ERROR)
def varinterval_validator(actual: xr.DataArray, expected: ParameterConfig) -> List[str]:
    """
    Take a bunch of random intervals in
    time, height, south_north, west_east
    and check if any datapoints are outside the interval
    Only done if dims correspond to expected dims
    """
    log.info("validating interval for %s", actual.name)
    dims = [str(dim) for dim in actual.dims]
    accept = get_acceptable_dims_from_parameter_key(str(actual.name))

    result = []
    if dims not in accept:
        return [
            f"Unsupported dimensional layout {dims}. Cannot evaluate interval. Accepted dimensional"
            f" layouts: {accept}"
        ]
    if validation_settings.should_check_min_max_full():
        # Long running operation, so have to explicitly request this in args
        result += none_less_than_min_validator(actual, expected)
        result += none_larger_than_max_validator(actual, expected)
        return result
    # Seed the randomizer. We want what is called here to be reproducible
    if validation_settings.should_skip_min_max_check():
        return []
    return _check_randomly_selected_intervals_min_max(actual, expected, dims)


def _check_randomly_selected_intervals_min_max(
    actual: xr.DataArray, expected: ParameterConfig, dims: List[str]
):
    rand = random.Random(SEED)
    result = []

    slice_tuple = _get_slice_tuple(dims, actual, rand)
    vals = actual[slice_tuple]
    vals.load()
    result += undermin_validator(actual, expected, slice_tuple, vals)
    result += overmax_validator(actual, expected, slice_tuple, vals)

    return result


@validation_node(severity=Severity.ERROR)
def undermin_validator(
    actual: xr.DataArray,
    expected: ParameterConfig,
    slice_tuple: Tuple[Union[int, slice], ...],
    vals: xr.DataArray,
) -> List[str]:
    """Check if any of the values in vals:DataArray retrieved
    from actual:DataArray are below minimum expected"""
    smallest = None
    if not isinstance(expected.min, str):
        smallest = round(
            float(vals.min().values), expected.number_of_significant_decimals
        )
        if smallest < expected.min:
            return [
                f"some values of {actual.name} were less than configured min {expected.min} for the"
                f" subcube {slice_tuple}. Minimum value was {smallest}"
            ]
    return []


@validation_node(severity=Severity.ERROR)
def overmax_validator(
    actual: xr.DataArray,
    expected: ParameterConfig,
    slice_tuple: Tuple[Union[int, slice], ...],
    vals: xr.DataArray,
) -> List[str]:
    """Check if any of the values in vals:DataArray retrieved
    from actual:DataArray are below minimum expected"""
    largest = None
    if not isinstance(expected.max, str):
        largest = round(
            float(vals.max().values), expected.number_of_significant_decimals
        )
        if largest > expected.max:
            return [
                f"some values of {actual.name} were higher than configured max {expected.max} for the"
                f" subcube {slice_tuple}. Maximum value was {float(largest)}"
            ]
    return []
