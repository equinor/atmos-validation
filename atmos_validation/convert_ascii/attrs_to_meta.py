import json
from typing import Dict

from ..schemas import DataType, MeasurementMetadata
from .utils import get_encoding


def load_attrs_map(attrs_map_path: str) -> Dict[str, str]:
    with open(attrs_map_path, "r", encoding="utf-8") as attrs_map:
        return json.load(attrs_map)


def parse_measurement_attrs(file_name: str, attrs_map_path: str):
    encoding = get_encoding(file_name)
    with open(file_name, "r", encoding=encoding, errors="ignore") as local_file:
        lines = local_file.readlines()
        attrs = {}

        attrs_map = load_attrs_map(attrs_map_path)
        for line in lines:
            if line.startswith("%"):
                attrs.update(
                    {
                        metadata: (
                            *map(lambda s: s.strip(), filter(None, line.split(":"))),
                        )[-1]
                        for metadata, attr in attrs_map.items()
                        if line.replace("%", "")
                        .strip()
                        .lower()
                        .startswith(attr.lower())
                    }
                )

        attrs["final_reports"] = attrs["final_reports"].split(",")
        attrs["instrument_types"] = attrs["instrument_types"].upper()
        attrs["installation_type"] = attrs["installation_type"].upper()
        attrs["data_usability"] = attrs["data_usability"].upper()
        attrs["source_file"] = (
            file_name.replace("ø", "oe").replace("æ", "ae").replace("å", "aa")
        )  # NetCDF attrs can not have Norwegian letters
        if "asset" not in attrs:
            attrs["asset"] = "NA"
        return MeasurementMetadata(**attrs, data_type=DataType.MEASUREMENT)
