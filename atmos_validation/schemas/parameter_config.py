import uuid
from typing import Any, Dict, List, Literal, Tuple, Union

from pydantic import BaseModel, Extra, Field, validator

from .dim_constants import get_acceptable_dims_from_parameter_key


class DefaultVariable(BaseModel):
    """Describes a default variable for a QC Test."""

    name: str
    description: str = Field(default="")
    value: Union[int, float, Tuple, str]
    unit_description: str = Field(default="")


class QCTest(BaseModel):
    """Describes a test to be run on a given parameter. QC tests are defined by metocean.
    The default parameters are configured by those with admins access.
    """

    test_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    long_name: str = Field(default="")
    metocean_pkg_ref: str = Field(default="")  # standard_name field
    default_variables: List[DefaultVariable] = Field(default_factory=list)
    description: str = Field(default="")


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
    qc_tests: Dict[str, QCTest] = Field(default_factory=dict)

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
