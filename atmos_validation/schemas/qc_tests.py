from typing import List

from pydantic import BaseModel, validator

from atmos_validation.schemas.parameter_configs import validate_unique

from .parameter_config import QCTest


class QCTests(BaseModel, arbitrary_types_allowed=True):
    configs: List[QCTest]

    @validator("configs")
    @classmethod
    def validate_unique_keys(cls, qc_tests: List[QCTest]):
        """All qc_tests in a config should be unique"""
        validate_unique(key_name="metocean_pkg_ref", entities=qc_tests)
        return qc_tests
