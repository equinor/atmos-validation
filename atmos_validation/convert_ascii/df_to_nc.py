import os
from typing import Any, Dict, Tuple

import pandas as pd
import xarray as xr

from ..schemas import dim_constants
from .attrs_to_meta import parse_measurement_attrs
from .parsers import data_frame_parser, parse_location_text, parse_parameter_meta
from .utils import (
    assign_datetime,
    get_attrs_for_key,
    get_config_for_key,
    get_encoding,
    get_heights_for_key,
    store_netcdf,
)


def ascii_to_nc(source_file: str) -> str:
    df, parameter_meta = parse_file(source_file)
    ds = df_to_ds(df, parameter_meta)
    assign_metadata_to_ds(source_file, ds)
    return store_netcdf(source_file, ds)


def parse_file(source_file: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    encoding = get_encoding(source_file)
    with open(source_file, "r", encoding=encoding, errors="ignore") as local_file:
        lines = local_file.readlines()
        header_line_number = 0
        parameters_start = 0
        parameter_meta = {}
        for line_number, line_content in enumerate(lines):
            if line_content.startswith("% Location"):
                loc_lat, loc_lon = parse_location_text(line_content)
                parameter_meta["loc_lat"] = loc_lat
                parameter_meta["loc_lon"] = loc_lon
            if line_content.startswith("% Hour"):
                parameters_start = line_number + 1
            if line_content.startswith("% Minute"):
                parameters_start = line_number + 1
            if not line_content.startswith("%"):
                header_line_number = line_number - 1
                break

        df = data_frame_parser(
            header_line=lines[header_line_number],
            data_lines=[line.split() for line in lines[header_line_number + 1 :]],
        )

        parameters_lines = lines[parameters_start:header_line_number]
        parameter_meta = parse_parameter_meta(parameters_lines, parameter_meta)

        return df, parameter_meta


def df_to_ds(df: pd.DataFrame, parameter_meta: Dict[str, Any]) -> xr.Dataset:
    data_arrays = {}
    lat = parameter_meta.pop("loc_lat")
    lon = parameter_meta.pop("loc_lon")
    df = assign_datetime(df)
    for key, key_meta in parameter_meta.items():
        attrs = get_attrs_for_key(key, instruments=str(key_meta["instruments"]))
        heights = get_heights_for_key(key, key_meta)

        columns = key_meta.get("key_columns")
        data = df.filter(columns).to_numpy()
        coords = {
            "Time": df["datetime"].values.astype("datetime64"),
            "LAT": (["south_north", "west_east"], [[lat]]),
            "LON": (["south_north", "west_east"], [[lon]]),
        }

        if heights:
            shape = len(df["datetime"]), len(heights), 1, 1
            dims = ("Time", "height_" + key, "south_north", "west_east")
            coords[f"{dim_constants.HEIGHT_DIM_PREFIX}{key}"] = heights
        else:
            shape = len(df["datetime"]), 1, 1
            dims = ("Time", "south_north", "west_east")

        data = data.reshape(shape)
        data_array = xr.DataArray(data, dims=dims, coords=coords, attrs=attrs)
        if heights:
            data_array = data_array.sortby(f"height_{key}")
        data_arrays[key] = data_array

    return enrich_coord_attrs(xr.Dataset(data_arrays))


def enrich_coord_attrs(ds: xr.Dataset) -> xr.Dataset:
    lon_cfg = get_config_for_key("LON_T")
    lat_cfg = get_config_for_key("LAT_T")
    ds.Time.attrs["CF_standard_name"] = "time"
    ds.LON.attrs["long_name"] = lon_cfg.long_name
    ds.LON.attrs["short_name"] = lon_cfg.short_name
    ds.LON.attrs["CF_standard_name"] = lon_cfg.CF_standard_name
    ds.LON.attrs["description"] = "Longitude"
    ds.LON.attrs["units"] = lon_cfg.units
    ds.LAT.attrs["long_name"] = lat_cfg.long_name
    ds.LAT.attrs["short_name"] = lat_cfg.short_name
    ds.LAT.attrs["CF_standard_name"] = lat_cfg.CF_standard_name
    ds.LAT.attrs["description"] = "Latitude"
    ds.LAT.attrs["units"] = lat_cfg.units
    for coord in ds.coords:
        if str(coord).startswith(dim_constants.HEIGHT_DIM_PREFIX):
            ds[coord].attrs["units"] = "m"
            ds[coord].attrs["CF_standard_name"] = "height"
            ds[coord].attrs["long_name"] = (
                f"Height for parameter {str(coord).replace(dim_constants.HEIGHT_DIM_PREFIX, '')}"
            )

    return ds


def assign_metadata_to_ds(source_file: str, ds: xr.Dataset):
    measurement_meta = parse_measurement_attrs(
        source_file,
        os.path.join(os.path.dirname(__file__), "measurement_metadata_to_schema.json"),
    )
    ds.attrs = measurement_meta.dict()
