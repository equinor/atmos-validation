import xarray as xr

from ...schemas.dim_constants import TIME
from ..validators.dims.time_validator import cf_standard_time_validator


def test_cf_standard_time_validation_ok():
    """
    Test that variable "Time" has value "time" as CF_standard_name passes
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds[TIME].attrs["CF_standard_name"] = "time"
        errors = cf_standard_time_validator(ds)
        assert len(errors) == 0


def test_cf_standard_time_validation_not_ok():
    """
    Test that variable "Time" has value "Time" as CF_standard_name does not pass
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds[TIME].attrs["CF_standard_name"] = "Time"  # capital T error
        errors = cf_standard_time_validator(ds)
        assert len(errors) == 1
        assert "Time" in errors[0]
        assert """should be "time".""" in errors[0]


def test_cf_standard_time_validation_not_found():
    """
    Test that missing CF_standard_name gives proper error output
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        del ds[TIME].attrs["CF_standard_name"]
        errors = cf_standard_time_validator(ds)
        assert len(errors) == 1
        assert "missing attribute" in errors[0]
