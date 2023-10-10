import xarray as xr

from ..validators.variables.varattrs_validator import var_height_depth_validator


def test_atmosphere_height_validation_ok():
    """
    Checks that the validator passes when the "height_" values associated
    with the "parameter_category" type "Atmosphere" are positive.
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        errors = var_height_depth_validator("P", ds, "Atmosphere")
        assert len(errors) == 0


def test_atmosphere_height_validation_not_ok_negative():
    """
    Checks that the validator fails when the "height_" values associated
    with the "parameter_category" type "Atmosphere" are negative.
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["height_WD"] = [5.00, -17.00]  # contains negative values
        errors = var_height_depth_validator("WD", ds, "Atmosphere")
        assert len(errors) == 1
        assert "Variables of category 'Atmosphere' must be positive." in errors[0]


def test_atmosphere_depth_validation_ok():
    """
    Checks that the validator passes when the "height_" values associated
    with "parameter_category" type "Ocean" are negative.
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["height_SST"] = [-17.00, -27.00]
        errors = var_height_depth_validator("SST", ds, "Ocean")
        assert len(errors) == 0


def test_atmosphere_depth_validation_not_ok_positive():
    """
    Checks that the validator fails when the "height_" values associated
    with "parameter_category" type "Ocean" are positive.
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["height_SST"] = [-1.00, 17.00, -100]
        errors = var_height_depth_validator("SST", ds, "Ocean")
        assert len(errors) == 1
        assert "Variables of category 'Ocean' must be negative." in errors[0]
