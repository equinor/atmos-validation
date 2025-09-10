from typing import List, Set

import xarray as xr

from ....schemas import get_acceptable_dims_from_parameter_key
from ...utils import Severity, validation_node


@validation_node(severity=Severity.ERROR)
def dimvars_validator(
    ds: xr.Dataset,
) -> List[str]:
    """
    This will verify that all variables have valid dimensions including
    name of height/depth dims if present
    and that all dimensions are attached to at least one variable.
    Incidentally, this also verifies that height/depth dimensions are
    correctly attached
    """
    alldims = {str(key) for key in ds.sizes.keys()}
    result = []
    for var in ds.keys():
        var = str(var)
        accept = get_acceptable_dims_from_parameter_key(var)
        actual = list(ds[var].dims)
        alldims -= set(actual).intersection(alldims)

        result += acceptable_vardims_validator(var, accept, actual)
    result += all_dims_must_have_variable_validator(alldims)
    return result


@validation_node(severity=Severity.ERROR)
def acceptable_vardims_validator(
    var: str, accept: List[List[str]], actual: List[str]
) -> List[str]:
    if actual not in accept:
        return [f"{var} has dims {actual}, but only {accept} is valid"]
    return []


@validation_node(severity=Severity.ERROR)
def all_dims_must_have_variable_validator(
    alldims_except_dims_attached_to_variables: Set[str],
) -> List[str]:
    if len(alldims_except_dims_attached_to_variables) > 0:
        return [
            "The following dimensions are not attached to a variable:"
            f" {alldims_except_dims_attached_to_variables}"
        ]
    return []
