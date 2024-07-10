import xarray as xr

from ..validators.file_attributes import data_usability_validator


def test_data_usability_validations_ok_single():
    """Tests when a single data usability level is valid"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["data_usability"] = "GENERIC STUDY"
        errors = data_usability_validator(ds)
        assert len(errors) == 0


def test_data_usability_validations_not_ok_single():
    """Tests when a single data usability level is invalid"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["data_usability"] = "INVALID"
        errors = data_usability_validator(ds)
        assert len(errors) == 1
        assert """Data usability "INVALID" is not in the allowed list.""" in errors[0]


def test_data_usability_validations_ok_multi():
    """Tests when multiple data usability levels are valid"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["data_usability"] = "RAW, NA"
        errors = data_usability_validator(ds)
        assert len(errors) == 0


def test_data_usability_validations_not_ok_multi():
    """Tests when several of many data usability levels are invalid"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["data_usability"] = (
            "RAW, INVALID, PROCESSED, ALSO INVALID, GENERIC STUDY"
        )
        errors = data_usability_validator(ds)
        assert len(errors) == 2
        assert """Data usability "INVALID" is not in the allowed list.""" in errors[0]
        assert (
            """Data usability "ALSO INVALID" is not in the allowed list.""" in errors[1]
        )
