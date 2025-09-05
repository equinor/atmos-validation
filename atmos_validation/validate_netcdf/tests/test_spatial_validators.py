import xarray as xr

from ...schemas import SOUTH_NORTH, WEST_EAST
from ..validators.dims.spatial_validators import (
    south_north_validator,
    west_east_validator,
)


def test_existence_validator_no_dim():
    errors = south_north_validator(xr.Dataset())
    assert len(errors) == 1
    assert f"{SOUTH_NORTH} is not a dimension in dataset" in errors[0]


def test_existence_validator_dim_length_0():
    ds = xr.Dataset()
    errors = west_east_validator(ds.expand_dims({WEST_EAST: []}))
    assert len(errors) == 1
    assert "has length 0" in errors[0]
