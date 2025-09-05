import json
from functools import lru_cache
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import pandas as pd
import requests
import xarray as xr
from pydantic import TypeAdapter

from ..schemas import ParameterConfig, ParameterConfigs

DEFAULT_URL_TO_PARAMETERS: str = "https://atmos.app.radix.equinor.com/config/parameters"


def get_chunksizes(dims: Tuple[str], src: xr.Dataset) -> Union[tuple[int, ...], None]:
    """Returns chunksizes for 3D or 4D data var.

    Args:
        dims: the dimensions associated with the data var
        src: the source xarray dataset

    Returns:
        chunksizes as a list or None if dims are not 3D or 4D
    """
    chunksizes = None
    if len(dims) == 4:
        chunksizes = (
            min(10000, len(src[dims[0]])),
            min(10, len(src[dims[1]])),
            1,
            1,
        )
    elif len(dims) == 3:
        chunksizes = (len(src[dims[0]]), 1, 1)

    return chunksizes


def translate_key(key: str) -> str:
    """Translates "wrong" base keys from raw measurement files into the expected keys according to the
    congfigured parameters.

    Args:
        key: The raw key parsed from the measurement file

    Returns:
        The corresponding key in the configured parameters table
    """
    translations = {
        "T1_TOT": "T01_TOT",
        "T1_SEA": "T01_SEA",
        "T1_SW": "T01_SW",
        "T2_TOT": "T02_TOT",
        "T2_SEA": "T02_SEA",
        "T2_SW": "T02_SW",
        "VBT": "BAT",
        "LAT": "LAT_T",
        "LON": "LON_T",
        "DEPTH": "DEPTH_T",
    }
    key = translations.get(key, key)
    return key


@lru_cache()
def get_config_for_key(key: str) -> ParameterConfig:
    configured_parameters = load_parameter_config_from_endpoint()
    return next(cfg for cfg in configured_parameters if cfg.key == key)


@lru_cache()
def load_parameter_config_from_endpoint() -> List[ParameterConfig]:
    response = requests.get(DEFAULT_URL_TO_PARAMETERS, timeout=10)
    adapter = TypeAdapter(List[ParameterConfig])
    cfgs = ParameterConfigs(configs=adapter.validate_json(json.dumps(response.json())))
    return cfgs.configs


def get_encoding(src_filename: str) -> str:
    if src_filename.endswith(".dat"):
        return "ascii"
    if src_filename.endswith(".txt"):
        return "ISO-8859-1"
    return "UTF-8"


def store_netcdf(source_file: str, ds: xr.Dataset) -> str:
    nc_filename = generate_nc_filename(source_file)
    ds.to_netcdf(
        nc_filename,
        encoding={
            "Time": {
                "dtype": "float64",
                "units": "microseconds since 1900-01-01 00:00:00",
            },
            **{
                var: {"zlib": True, "chunksizes": get_chunksizes(ds[var].dims, ds)}  # type: ignore
                for var in ds.data_vars
            },
        },
        unlimited_dims="Time",
        engine="h5netcdf",
    )
    return nc_filename


def generate_nc_filename(source_file: str) -> str:
    nc_filename = source_file.removesuffix(".dat")
    nc_filename = nc_filename.removesuffix(".txt")
    nc_filename = nc_filename.removesuffix(".LIS")
    nc_filename = nc_filename.replace(" ", "_")
    nc_filename = nc_filename.replace(",", "_")
    nc_filename = nc_filename.replace("__", "_")
    return f"{nc_filename}.nc"


def assign_datetime(df: pd.DataFrame) -> pd.DataFrame:
    column_map = {"YY": "year", "MM": "month", "DD": "day", "HH": "h"}
    columns = ["YY", "MM", "DD", "HH"]
    if "Min" in df:
        columns.append("Min")
        column_map["Min"] = "m"
    df["datetime"] = pd.to_datetime(df[columns].rename(columns=column_map))  # type: ignore
    return df


def get_attrs_for_key(key: str, instruments: str) -> Dict[str, Any]:
    cfg = get_config_for_key(key)
    return {
        "units": cfg.units,
        "CF_standard_name": cfg.CF_standard_name,
        "long_name": cfg.long_name,
        "instruments": instruments,
    }


def get_heights_for_key(
    key: str, key_meta: Dict[str, Any]
) -> Union[List[Union[int, float]], None]:
    cfg = get_config_for_key(key)
    is_depth = 1
    if cfg.parameter_category == "Ocean":
        is_depth = -1
    heights = key_meta.get("heights")
    if heights:
        heights = is_depth * np.abs(heights)
        return list(heights)
    return heights
