"""
Note that doing the settings like this, assumes that all runs for the application will use same settings.
If this ever becomes an issue, an easy refactor would be to make the settings a dict based on system name.
The other option would be to pass the settings down the entire tree of validators.
"""

from contextvars import ContextVar
from typing import FrozenSet, List

CHECK_MIN_MAX_FULL: str = "--check-min-max-full"
SKIP_MIN_MAX_CHECK: str = "--skip-random-min-max-check"
SKIP_WARNINGS: str = "--skip-warnings"
URL_TO_PARAMETERS: str = "https://atmos.app.radix.equinor.com/config/parameters"
URL_TO_INST_TYPES: str = "https://atmos.app.radix.equinor.com/config/installation-types"
URL_TO_DATA_USABILITY: str = "https://atmos.app.radix.equinor.com/config/data-usability"

# Per-call, thread/async-isolated so options never leak between validate() calls.
_active_settings: ContextVar[FrozenSet[str]] = ContextVar(
    "validation_settings", default=frozenset()
)


def apply_settings(optional_args: List[str]) -> None:
    _active_settings.set(frozenset(optional_args))


def should_skip_min_max_check() -> bool:
    return SKIP_MIN_MAX_CHECK in _active_settings.get()


def should_check_min_max_full() -> bool:
    return CHECK_MIN_MAX_FULL in _active_settings.get()


def should_skip_warnings() -> bool:
    return SKIP_WARNINGS in _active_settings.get()
