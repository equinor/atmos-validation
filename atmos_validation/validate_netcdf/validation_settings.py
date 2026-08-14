"""
Note that doing the settings like this, assumes that all runs for the application will use same settings.
If this ever becomes an issue, an easy refactor would be to make the settings a dict based on system name.
The other option would be to pass the settings down the entire tree of validators.
"""

import random
import sys
from contextvars import ContextVar
from typing import FrozenSet, List

from .validation_logger import log

CHECK_MIN_MAX_FULL: str = "--check-min-max-full"
SKIP_MIN_MAX_CHECK: str = "--skip-random-min-max-check"
SKIP_WARNINGS: str = "--skip-warnings"
RANDOM_SEED: str = "--random-seed"
SAMPLE_SIZE: str = "--sample-size"
DEFAULT_SAMPLE_SIZE: int = 5000
URL_TO_PARAMETERS: str = "https://atmos.app.radix.equinor.com/config/parameters"
URL_TO_INST_TYPES: str = "https://atmos.app.radix.equinor.com/config/installation-types"
URL_TO_DATA_USABILITY: str = "https://atmos.app.radix.equinor.com/config/data-usability"

# Per-call, thread/async-isolated so options never leak between validate() calls.
_active_settings: ContextVar[FrozenSet[str]] = ContextVar(
    "validation_settings", default=frozenset()
)
_random_seed: ContextVar[int] = ContextVar("random_seed")
_sample_size: ContextVar[int] = ContextVar("sample_size", default=DEFAULT_SAMPLE_SIZE)


def apply_settings(optional_args: List[str]) -> None:
    _active_settings.set(frozenset(optional_args))
    _random_seed.set(_parse_random_seed(optional_args))
    _sample_size.set(_parse_sample_size(optional_args))


def _parse_random_seed(optional_args: List[str]) -> int:
    for i, arg in enumerate(optional_args):
        if arg == RANDOM_SEED:
            if i + 1 >= len(optional_args):
                raise ValueError(f"{RANDOM_SEED} requires an integer value")
            return int(optional_args[i + 1])
        if arg.startswith(f"{RANDOM_SEED}="):
            seed = arg.split("=", 1)[1]
            log.info("using random seed: %s", seed)
            return int(seed)
    seed = random.randrange(sys.maxsize)  # default random seed if not specified
    log.info("using random seed: %s", seed)
    return seed


def get_random_seed() -> int:
    return _random_seed.get()


def _parse_sample_size(optional_args: List[str]) -> int:
    for i, arg in enumerate(optional_args):
        if arg == SAMPLE_SIZE:
            if i + 1 >= len(optional_args):
                raise ValueError(f"{SAMPLE_SIZE} requires an integer value")
            return int(optional_args[i + 1])
        if arg.startswith(f"{SAMPLE_SIZE}="):
            return int(arg.split("=", 1)[1])
    return DEFAULT_SAMPLE_SIZE


def get_sample_size() -> int:
    return _sample_size.get()


def should_skip_min_max_check() -> bool:
    return SKIP_MIN_MAX_CHECK in _active_settings.get()


def should_check_min_max_full() -> bool:
    return CHECK_MIN_MAX_FULL in _active_settings.get()


def should_skip_warnings() -> bool:
    return SKIP_WARNINGS in _active_settings.get()
