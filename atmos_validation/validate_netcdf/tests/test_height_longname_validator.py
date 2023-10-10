import xarray as xr

from ..validators.variables.varattrs_validator import var_height_longname_validator


def test_height_long_name_ok():
    """
    Checks that the validator passes when the 'long_name' for 'height_XX' is valid.
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        errors = var_height_longname_validator("P", ds)
        assert len(errors) == 0


def test_height_long_name_not_ok():
    """
    Checks that the validator fails when the 'long_name' for 'height_XX' is invalid.
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["height_WG"].attrs["long_name"] = "invalid_long_name"
        errors = var_height_longname_validator("WG", ds)
        assert len(errors) == 1
        assert """should have 'long_name' set to """ in errors[0]
