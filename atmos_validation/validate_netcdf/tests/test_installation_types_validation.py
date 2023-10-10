import xarray as xr

from ..validators.file_attributes import installation_type_validator


def test_installation_type_validations_ok():
    """Tests that installation_type validator when type is invalid"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["installation_type"] = "BUOY"
        errors = installation_type_validator(ds)
        assert len(errors) == 0


def test_installation_type_validations_not_ok():
    """Tests that installation_type validator when type is invalid"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["installation_type"] = "INVALID"
        errors = installation_type_validator(ds)
        assert len(errors) == 1
        assert "not in the allowed list" in errors[0]
