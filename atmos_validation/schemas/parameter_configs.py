from typing import Any, List

from pydantic import BaseModel, validator

from .parameter_config import ParameterConfig


class ParameterConfigs(BaseModel, arbitrary_types_allowed=True):
    configs: List[ParameterConfig]

    @validator("configs")
    @classmethod
    def validate_unique_keys(cls, parameters: List[ParameterConfig]):
        """All keys in a config should be unique"""
        validate_unique(key_name="key", entities=parameters)
        return parameters

    @property
    def param_dict(self):
        return {p.key: p for p in self.configs}


def validate_unique(key_name: str, entities: List[Any]):
    """Validates that a given key in a list of entities is unique

    Args:
        key_name: the identifier that should be unique on the object
        entities: the list of entities to assert uniqueness on

    Raises:
        ValueError: if entities have non-unique key_name, raise error
    """
    duplicates = set()
    checked = set()
    for entity in entities:
        key = getattr(entity, key_name)
        if key not in checked:
            checked.add(key)
        else:
            duplicates.add(key)
    if len(duplicates) > 0:
        raise ValueError(f"Found duplicate keys in config, duplicates: {duplicates}")
