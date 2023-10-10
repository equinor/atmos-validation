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
    errors = south_north_validator(ds.expand_dims({SOUTH_NORTH: []}))
    assert len(errors) == 1
    assert "has length 0" in errors[0]


def test_place_validator():
    ds = xr.Dataset()
    ds = ds.expand_dims({SOUTH_NORTH: [0, 1], WEST_EAST: [0, 1]})
    ds = ds.assign(P=((WEST_EAST, SOUTH_NORTH), [[0, 1], [2, 3]]))  # wrong order
    errors = south_north_validator(ds)
    errors += west_east_validator(ds)
    assert len(errors) == 2
    assert f"P does not have {SOUTH_NORTH} at dimension index -2" in errors[0]
    assert f"P does not have {WEST_EAST} at dimension index -1" in errors[1]
