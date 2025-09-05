import re
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from ..schemas import dim_constants
from .utils import get_config_for_key, translate_key

MISSING_HEIGHT = -99999


def parse_location_text(line_content: str) -> Tuple[float, float]:
    """Parses Location text into a float tuple (lat, lon)

    Args:
        line_content: the raw location text line

    Returns:
        float numbers tuple (lat, lon)
    """
    location_text = line_content.split(":", 1)[1].split(",")[0]
    location_text = location_text.replace("Â", "")
    match = re.findall(r"[-+]?(?:\d*\.*\d+)", location_text)
    is_east = 1
    is_north = 1
    if "S" in location_text:
        is_north = -1
    if "W" in location_text:
        is_east = -1
    return (float(match[0]) * is_north, float(match[1]) * is_east)


def data_frame_parser(header_line: str, data_lines: List[List[str]]) -> pd.DataFrame:
    """Parses the header line and the data_lines into a pandas df

    Args:
        header_line: the raw header line to be parsed into column headers
        data_lines: a list of string lists containing the values on each row

    Returns:
        pandas df with headers given by header line and data given by data_lines
    """
    header_names = header_line.replace("%", "").replace("\t\n", "").split()
    df = pd.DataFrame(
        data=data_lines,
        columns=header_names,  # type: ignore
    )

    df = df.dropna(how="all")
    df = df.replace("-999", np.nan)
    df = df.replace("-999.99", np.nan)
    df = df.replace("NaN", np.nan)
    for col in df:
        if str(col).lower() not in ["yy", "mm", "dd", "hh", "min"]:
            df[col] = df[col].astype(np.float32)
    df["YY"] = df["YY"].astype(int)
    df["MM"] = df["MM"].astype(int)
    df["DD"] = df["DD"].astype(int)
    df["HH"] = df["HH"].astype(int)
    if "Min" in df:
        df["Min"] = df["Min"].astype(int)

    return df


def parse_parameter_meta(
    parameters_lines: List[str],
    parameter_meta: Dict[str, Any],
) -> Dict[str, Any]:
    for line in parameters_lines:
        parsed_line = parse_line(line)
        if parsed_line == ["%"]:
            continue
        (
            _,
            new_abbrev,
            new_unit,
            new_height,
            new_key,
            new_inst_type,
            new_inst_spec,
        ) = parse_line(line)
        instrument_types = new_inst_type.upper().split(",")
        instrument_specs = new_inst_spec.split(",")
        new_instruments = [
            f"{inst_type.strip()}, {inst_spec.strip()}"
            for inst_type, inst_spec in zip(instrument_types, instrument_specs)
        ]
        new_key = translate_key(new_key)
        cfg = get_config_for_key(new_key)
        should_have_height = f"{dim_constants.HEIGHT_DIM_PREFIX}{new_key}" in cfg.dims

        if not should_have_height:
            enrich_param(
                new_key,
                new_abbrev,
                new_unit,
                new_instruments,
                parameter_meta,
            )
        else:
            try:
                new_height = float(new_height)
            except Exception:
                new_height = MISSING_HEIGHT

            enrich_heighted_param(
                new_key,
                new_abbrev,
                new_height,
                new_unit,
                new_instruments,
                parameter_meta,
            )

    return parameter_meta


def parse_line(line: str):
    try:
        line_values = list(
            filter(
                lambda line: line != "",
                line.strip().replace("\n", "").split("  "),
            )
        )
        assert len(line_values) == 7
    except Exception:
        line_values = list(
            filter(
                lambda line: line != "",
                line.strip().replace("\n", "").split("\t"),
            )
        )
    line_values = [val.strip() for val in line_values]
    return line_values


def enrich_param(
    new_key: str,
    new_abbrev: str,
    new_unit: str,
    new_instruments: List[str],
    parameter_meta: Dict[str, Any],
):
    key_meta = {
        "unit": new_unit,
        "key_columns": [new_abbrev],
        "heights": None,
        "instruments": {new_inst: [] for new_inst in new_instruments},
    }
    parameter_meta[new_key] = key_meta


def enrich_heighted_param(  # pylint: disable=too-many-arguments
    new_key: str,
    new_abbrev: str,
    new_height: float,
    new_unit: str,
    new_instruments: List[str],
    parameter_meta: Dict[str, Any],
):
    if new_key not in parameter_meta:
        key_meta = {
            "unit": new_unit,
            "key_columns": [new_abbrev],
            "heights": [new_height],
            "instruments": {instrument: [new_height] for instrument in new_instruments},
        }
        parameter_meta[new_key] = key_meta
    else:
        key_meta = parameter_meta.get(new_key, {})

        key_meta.get("heights").append(new_height)
        key_meta.get("key_columns").append(new_abbrev)

        if key_meta.get("unit") != new_unit:
            raise ValueError(f"Not consistent units for all heights in key {new_key}")

        instruments = key_meta.get("instruments")
        for inst_key in new_instruments:
            if instruments.get(inst_key):
                instruments.get(inst_key).append(new_height)
            else:
                instruments[inst_key] = [new_height]
