from typing import List

from pydantic import BaseModel, validator

from .instrument_type import InstrumentType
from .parameter_configs import validate_unique


class InstrumentTypes(BaseModel, arbitrary_types_allowed=True):
    configs: List[InstrumentType]

    @validator("configs")
    @classmethod
    def validate_unique_keys(cls, instruments: List[InstrumentType]):
        """All instrument_types in a config should be unique"""
        validate_unique(key_name="instrument_type", entities=instruments)
        return instruments
