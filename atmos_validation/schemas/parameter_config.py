from typing import Any, Dict, List, Literal, Union

from pydantic import BaseModel, Extra, validator

from .dim_constants import get_acceptable_dims_from_parameter_key


class ParameterConfig(BaseModel, arbitrary_types_allowed=True, extra=Extra.allow):
    key: str
    parameter_category: str
    parameter_type: str
    short_name: str
    long_name: str
    description: str
    allowed_instruments: List[str]
    number_of_significant_decimals: int
    units: str
    min: Union[float, int, Literal["NA"]]
    max: Union[float, int, Literal["NA"]]
    CF_standard_name: str
    dims: List[str]

    @validator("dims")
    @classmethod
    def validate_dims(cls, dims: List[str], values: Dict[str, Any]):
        key = values["key"]
        accept = get_acceptable_dims_from_parameter_key(key)
        for accepted_dims in accept:
            if accepted_dims == dims:
                return dims
        raise ValueError(
            f"Unacceptable dims list {dims} for key {key}. Possible lists are {accept}"
        )

    def get_required_attributes(self, is_measurement: bool) -> List[str]:
        extras = []
        if is_measurement:
            extras += ["instruments"]
        return list(self.get_required_values().keys()) + extras

    def get_required_values(self) -> Dict[str, Any]:
        """
        Used in validation for NCDF attributes on system parameters. Used both for
        ensuring the attributes are set and that values are according to configuration.
        """
        return {
            "units": self.units,
            "CF_standard_name": self.CF_standard_name,
            "long_name": self.long_name,
        }
