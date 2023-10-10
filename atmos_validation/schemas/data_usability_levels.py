from typing import List

from pydantic import BaseModel, validator

from .data_usability_level import DataUsabilityLevel
from .parameter_configs import validate_unique


class DataUsabilityLevels(BaseModel, arbitrary_types_allowed=True):
    configs: List[DataUsabilityLevel]

    @validator("configs")
    @classmethod
    def validate_unique_keys(cls, usability_levels: List[DataUsabilityLevel]):
        """All instrument_types in a config should be unique"""
        validate_unique(key_name="level", entities=usability_levels)
        return usability_levels
