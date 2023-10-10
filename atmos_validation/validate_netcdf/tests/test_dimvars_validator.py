from atmos_validation.schemas import dim_constants

from ..validators.dims.dimvars_validator import (
    acceptable_vardims_validator,
    all_dims_must_have_variable_validator,
)


def test_acceptable_vardims_validator():
    errors = acceptable_vardims_validator(
        var="SST", accept=[dim_constants.TIME], actual=["not accepted"]
    )
    assert len(errors) == 1


def test_all_dims_must_have_variable_validator():
    errors = all_dims_must_have_variable_validator(
        alldims_except_dims_attached_to_variables=set("height_P")
    )
    assert len(errors) == 1
