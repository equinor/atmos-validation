from typing import List

import xarray as xr

from ..utils import Severity
from ..validation_logger import log
from .dims.dims_validator import dims_validator
from .file_attributes import file_attributes_validator
from .variables.variables_validator import variables_validator


class ValidationResult:
    def __init__(self, warnings: List[str], errors: List[str]) -> None:
        self.warnings = warnings
        self.errors = errors


def root_validator(ds: xr.Dataset, paths: List[str]) -> ValidationResult:
    log.debug("Launch root validator")

    results = (
        []
        + dims_validator(ds, paths)
        + variables_validator(ds)
        + file_attributes_validator(ds)
    )
    warnings = [output for output in results if Severity.WARNING in output]
    errors = [output for output in results if Severity.WARNING not in output]

    return ValidationResult(warnings=warnings, errors=errors)
