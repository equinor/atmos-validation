from typing import List

from pydantic import BaseModel, field_validator

from .installation_type import InstallationType
from .parameter_configs import validate_unique


class InstallationTypes(BaseModel):
    configs: List[InstallationType]

    @field_validator("configs")
    @classmethod
    def validate_unique_keys(cls, installation_types: List[InstallationType]):
        """All instrument_types in a config should be unique"""
        validate_unique(key_name="installation_type", entities=installation_types)
        return installation_types
