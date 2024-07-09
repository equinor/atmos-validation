import json
from functools import lru_cache
from typing import Dict, List, Set

import requests
from pydantic import TypeAdapter

from ..schemas import ParameterConfig, ParameterConfigs
from .header_names import Headers


def trim_value(value: str) -> str:
    return value.replace("\t", "").strip()


def get_all_accepted_metadata_values() -> Dict[str, Set[str]]:
    base_url = "https://atmos.app.radix.equinor.com/config"
    get_options = [
        ("/instrument-types", "instrument_type"),
        ("/installation-types", "installation_type"),
        ("/data-usability", "level"),
    ]
    result: Dict[str, Set[str]] = {
        Headers.INSTRUMENTS: set(),
        Headers.INSTALLATION_TYPE: set(),
        Headers.DATA_USTABILITY_LEVEL: set(),
    }

    for opts, key in zip(get_options, result.keys()):
        path, get_key = opts
        items = requests.get(base_url + path, timeout=10).json()
        for item in items:
            result[key].add(item[get_key])
    return result


@lru_cache()
def load_parameter_configs() -> List[ParameterConfig]:
    response = requests.get(
        "https://atmos.app.radix.equinor.com/config/parameters", timeout=10
    )
    adapter = TypeAdapter(List[ParameterConfig])
    cfgs = ParameterConfigs(configs=adapter.validate_json(json.dumps(response.json())))
    return cfgs.configs
