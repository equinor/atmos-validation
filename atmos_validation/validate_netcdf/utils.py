import os
import traceback
from enum import Enum
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, TypeVar

import pandas as pd
import xarray as xr

from atmos_validation.validate_netcdf import validation_settings

from .validation_logger import log


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


def get_file_paths_in_folder(folder_path: str, filetype: str = ".nc") -> List[str]:
    paths = []
    for _, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(filetype):
                filepath = os.path.join(folder_path, filename)
                paths.append(filepath)
        break
    return paths


def validation_node(
    severity: Severity,
    node_name: Optional[str] = None,
    postfix: Optional[Callable[[Tuple[Any, ...], Dict[str, Any]], str]] = None,
) -> Callable[[Callable[..., List[str]]], Callable[..., List[str]]]:
    """
    All validators should be wrapped in this. Enforces some common functionality,
    such as transforming an exception to a message so that all other validators may keep
    firing. Also enforces a validator naming scheme to make the code-base consistent.
    Prefixes all messages with the full path through the nodes to the validator
    for a structured response e.g root:dims:heights:height:<message>.


    Parameters
    ----------
    severity: a string token to signal the severity of the error output from this validation node.
    node_name: names the node in the return. Pass a callable to use one of the named arguments
    postfix: a callable on the *args **kwargs of the wrapped function.
    The return is added as a postfix to the node name
    """

    def outer(func: Callable[..., List[str]]) -> Callable[..., List[str]]:
        def validation_node_wrapper(*args: Any, **kwargs: Any) -> List[str]:
            if (
                validation_settings.should_skip_warnings()
                and severity == Severity.WARNING
            ):
                return []

            nonlocal node_name
            local_name = node_name
            if not func.__name__.endswith("_validator") or len(func.__name__) < 13:
                raise NameError(
                    "validators should end with _validator and have more than 13 chars total"
                )
            if local_name is None:
                local_name = func.__name__[0:-10]
            local_name = local_name + ":"
            if postfix is not None:
                local_name = local_name + postfix(args, kwargs) + ":"
            try:
                errors = func(*args, **kwargs)
            except Exception as e:
                traceback.print_exc()
                message = f"Exception while executing validator {repr(e)}"
                errors = [message]
                log.error(
                    "Exception while executing validator %s",
                    local_name + message,
                    exc_info=True,
                )

            return [inject_severity(local_name, error, severity) for error in errors]

        validation_node_wrapper.__dict__["is_validation_node"] = True
        return validation_node_wrapper

    return outer


def inject_severity(local_name: str, error: str, severity: Severity):
    if any((severity_token.value in error for severity_token in Severity)):
        # return without injecting if string already contains a token
        return f"{local_name}{error}"
    return f"{local_name}{severity}:{error}"


def to_number_if_possible(maybe_number: Any) -> Any:
    if isinstance(maybe_number, str) and maybe_number.isdigit():
        return int(maybe_number)
    if isinstance(maybe_number, str):
        try:
            return float(maybe_number)
        except ValueError:
            return maybe_number
    return maybe_number


def almost_equal(first: Any, second: Any, diff: float = 0e-6) -> bool:
    """
    Checks for equality. Parses int or float if necessary.
    If other object than int or float, does an object ==
    """
    num_a = to_number_if_possible(first)
    num_b = to_number_if_possible(second)
    if isinstance(num_a, int) and isinstance(num_b, int):
        return num_a == num_b
    if isinstance(first, (float, int)) and isinstance(second, (float, int)):
        return abs(first - second) <= diff
    return first == second


T = TypeVar("T")


def first_or_none(
    collection: Iterable[T],
    predicate: Callable[[T], bool],
    throw_if_missing: bool = False,
) -> Tuple[Optional[int], Optional[T]]:
    """Find element in collection based on predicate, return index and item if found"""
    for i, item in enumerate(collection):
        if predicate(item):
            return i, item
    if throw_if_missing:
        raise ValueError("Missing value in collection")
    return None, None


def is_measurement(ds: xr.Dataset):
    try:
        return ds.attrs["data_type"] == "Measurement"
    except KeyError as e:
        log.error(
            "Did not find attribute 'data_type' on dataset."
            "Please set 'data_type' to either 'Measurement' or 'Hindcast'"
        )
        raise e


def convert_utc_timestamp_to_filename_format(utc_timestamp: int):
    return pd.to_datetime(
        utc_timestamp,
        unit="us",
        utc=True,
        origin="1900-01-01",
    ).strftime("%Y%m%d")
