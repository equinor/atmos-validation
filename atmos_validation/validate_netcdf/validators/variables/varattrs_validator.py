import ast
from typing import Any, Dict, List

import xarray as xr

from ....schemas.dim_constants import HEIGHT_DIM_PREFIX
from ...utils import Severity, almost_equal, is_measurement, validation_node


@validation_node(severity=Severity.ERROR)
def var_height_longname_validator(key: str, ds: xr.Dataset) -> List[str]:
    """Verify that 'long_name' for a given 'height_XX' is 'height for parameter height_XX'"""
    result = []
    try:
        # make case insensitive for first char
        actual_long_name = ds[HEIGHT_DIM_PREFIX + key].attrs["long_name"]
        if (
            actual_long_name[0].lower() + actual_long_name[1:]
            != f"height for parameter {key}"
        ):
            result += [
                f"The variable {key} should have 'long_name' set to 'height for parameter {key}'"
            ]

    except KeyError:
        # missing attributes are reported by "var_mandatory_attrs_validator"
        pass
    return result


@validation_node(severity=Severity.ERROR)
def var_mandatory_attrs_validator(
    var: str, actual: Dict[str, Any], expected: List[str]
) -> List[str]:
    result = []
    for key in expected:
        if key not in actual:
            result += [
                f"The mandatory attribute {key} does not exist in the variable {var}"
            ]
    return result


@validation_node(severity=Severity.ERROR)
def var_required_attr_values_validator(
    var: str, actual: Dict[str, Any], expected: Dict[str, Any]
) -> List[str]:
    "Verify attributes on variable"
    result = []
    for key, value in expected.items():
        actual_value = actual.get(key)
        if actual_value is None:
            result += [
                f"The variable {var} should have the value {value} for the attribute {key}. The"
                " attribute could not be found"
            ]
        elif not almost_equal(value, actual_value):
            result += [
                f"The variable {var} should have the value {value} for the attribute {key}. The"
                f" attribute had value {actual_value}"
            ]
    return result


@validation_node(severity=Severity.ERROR)
def var_allowed_instruments_validator(
    key: str, ds: xr.Dataset, allowed_instruments: List[str]
) -> List[str]:
    """Verify that instrument matches allowed instrument types if system type is measurement"""
    result = []

    if not is_measurement(ds):
        return result

    try:
        instruments: str = ds[key].attrs["instruments"]
        instruments_list = []
        try:
            instruments_dict: Dict[str, Any] = ast.literal_eval(instruments)
            instruments_list = [inst.split(",")[0] for inst in instruments_dict.keys()]
        except Exception:
            result += [f"instruments on variable {key} could not be parsed as a dict"]
            return result

        for instrument in instruments_list:
            if instrument not in allowed_instruments:
                result += [
                    f"""The variable "{key}" has wrong instrument_type value: """
                    f"""{instrument}". Allowed values: {allowed_instruments}"""
                ]
    except KeyError:
        # missing attributes are reported by "var_mandatory_attrs_validator"
        pass

    return result


@validation_node(severity=Severity.ERROR)
def var_height_depth_validator(
    key: str, ds: xr.Dataset, parameter_category: str
) -> List[str]:
    """
    Verify that variables of "parameter_category" type "Atmosphere" have positive
    height, and "Ocean" have negative depth.
    """
    result = []
    try:
        values = ds[f"{HEIGHT_DIM_PREFIX}{key}"]

        if parameter_category == "Atmosphere":
            for value in values:
                if value < 0:
                    result += [
                        f"""The variable "{key}" has invalid height, "{value}"."""
                        f"""Variables of category 'Atmosphere' must be positive."""
                    ]
        elif parameter_category == "Ocean":
            for value in values:
                if value > 0:
                    result += [
                        f"""The variable "{key}" has invalid depth, "{value}"."""
                        f"""Variables of category 'Ocean' must be negative."""
                    ]
    except KeyError:
        # missing attributes are reported by "var_mandatory_attrs_validator"
        pass
    return result
