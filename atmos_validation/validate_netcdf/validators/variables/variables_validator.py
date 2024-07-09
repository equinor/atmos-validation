import urllib.request
from typing import List

import xarray as xr
from pydantic import TypeAdapter

from ....schemas import ParameterConfig, ParameterConfigs
from ...utils import Severity, is_measurement, validation_node
from ...validation_logger import log
from ...validation_settings import get_url_to_parameters
from .sig_dig_validator import sig_dig_validator
from .varattrs_validator import (
    var_allowed_instruments_validator,
    var_height_depth_validator,
    var_height_longname_validator,
    var_mandatory_attrs_validator,
    var_required_attr_values_validator,
)
from .vardims_validator import vardims_validator
from .varinterval_validator import varinterval_validator


def load_parameter_config_from_endpoint():
    url = get_url_to_parameters()
    log.debug("download parameters config")
    with urllib.request.urlopen(url) as response:
        data = response.read()
        adapter = TypeAdapter(List[ParameterConfig])
        return ParameterConfigs(configs=adapter.validate_json(data))


@validation_node(severity=Severity.ERROR)
def variables_validator(ds: xr.Dataset) -> List[str]:
    valids = load_parameter_config_from_endpoint().param_dict
    errors = []
    for key in list(ds.keys()):
        if key not in valids:
            errors += [f"{key} is not a valid key"]
        else:
            errors += variable_validator(ds, key, valids[key])
    return errors


@validation_node(severity=Severity.ERROR, postfix=lambda args, _: args[1])
def variable_validator(
    ds: xr.Dataset, key: str, parameter_settings: ParameterConfig
) -> List[str]:
    var = ds[key]
    return (
        []
        + vardims_validator(key, var.dims, parameter_settings.dims)
        + var_mandatory_attrs_validator(
            key,
            var.attrs,
            parameter_settings.get_required_attributes(is_measurement(ds)),
        )
        + var_required_attr_values_validator(
            key, var.attrs, parameter_settings.get_required_values()
        )
        + var_allowed_instruments_validator(
            key, ds, parameter_settings.allowed_instruments
        )
        + varinterval_validator(var, parameter_settings)
        + sig_dig_validator(var, parameter_settings)
        + var_height_longname_validator(key, ds)
        + var_height_depth_validator(key, ds, parameter_settings.parameter_category)
    )
