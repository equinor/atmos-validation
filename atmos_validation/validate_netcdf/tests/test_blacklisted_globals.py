import xarray as xr

from ..validators.file_attributes import blacklisted_global_attributes_validator


def test_blacklisted_attributes_ok():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["data_type"] = "Measurement"
        errors = blacklisted_global_attributes_validator(ds)
        assert len(errors) == 0


def test_blacklisted_attributes_not_ok():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["data_type"] = "Hindcast"
        errors = blacklisted_global_attributes_validator(ds)
        assert len(errors) == 9
