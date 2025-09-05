"""
Note that doing the settings like this, assumes that all runs for the application will use same settings.
If this ever becomes an issue, an easy refactor would be to make the settings a dict based on system name.
The other option would be to pass the settings down the entire tree of validators.
"""

from typing import List

CHECK_MIN_MAX_FULL: str = "--check-min-max-full"
SKIP_MIN_MAX_CHECK: str = "--skip-random-min-max-check"
SKIP_WARNINGS: str = "--skip-warnings"
URL_TO_PARAMETERS: str = "--set-url-to-parameters="
DEFAULT_URL_TO_PARAMETERS: str = "https://atmos.app.radix.equinor.com/config/parameters"
BATCH_SIZE: str = "--batch-size="
DEFAULT_BATCH_SIZE = 1000
NO_OF_BATCHES: int
SETTINGS = set()


def apply_settings(optional_args: List[str]):
    for arg in optional_args:
        SETTINGS.add(arg)


def get_url_to_parameters() -> str:
    for arg in SETTINGS:
        if str(arg).startswith(URL_TO_PARAMETERS):
            return str(arg).split(URL_TO_PARAMETERS, 1)[1].strip()
    # Not supplied, return default
    return DEFAULT_URL_TO_PARAMETERS


def set_batch_size(override: int):
    batch_size_argument = None
    for arg in SETTINGS:
        if str(arg).startswith(BATCH_SIZE):
            batch_size_argument = arg

    if batch_size_argument:
        SETTINGS.remove(batch_size_argument)

    SETTINGS.add(f"{BATCH_SIZE}{override}")


def get_batch_size() -> int:
    batch_size = DEFAULT_BATCH_SIZE
    for arg in SETTINGS:
        if str(arg).startswith(BATCH_SIZE):
            try:
                batch_size = int(str(arg).split(BATCH_SIZE, 1)[1].strip())
            except ValueError as e:
                raise TypeError("Batch size must be an integer") from e
    print(f"using batch_size = {batch_size}")
    return batch_size


def should_skip_min_max_check() -> bool:
    return SKIP_MIN_MAX_CHECK in SETTINGS


def should_check_min_max_full() -> bool:
    return CHECK_MIN_MAX_FULL in SETTINGS


def should_skip_warnings() -> bool:
    return SKIP_WARNINGS in SETTINGS
