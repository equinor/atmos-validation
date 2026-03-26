from typing import List

from pydantic import BaseModel, field_validator

from .instrument_type import InstrumentType
from .parameter_configs import validate_unique


class InstrumentTypes(BaseModel):
    configs: List[InstrumentType]

    @field_validator("configs")
    @classmethod
    def validate_unique_keys(cls, instruments: List[InstrumentType]):
        """All instrument_types in a config should be unique"""
        validate_unique(key_name="instrument_type", entities=instruments)
        return instruments
