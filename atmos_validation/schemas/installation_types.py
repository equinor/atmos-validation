from typing import List

from pydantic import BaseModel, validator

from .installation_type import InstallationType
from .parameter_configs import validate_unique


class InstallationTypes(BaseModel, arbitrary_types_allowed=True):
    configs: List[InstallationType]

    @validator("configs")
    @classmethod
    def validate_unique_keys(cls, installation_types: List[InstallationType]):
        """All instrument_types in a config should be unique"""
        validate_unique(key_name="installation_type", entities=installation_types)
        return installation_types
