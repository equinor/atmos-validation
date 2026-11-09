import xarray as xr

from ..validators.file_attributes import instrument_counts_validator


def test_instrument_counts_validations_ok():
    """Tests that instrument_counts_validator passes when counts match"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        errors = instrument_counts_validator(ds)
        assert len(errors) == 0


def test_instrument_counts_validations_not_ok():
    """Tests that instrument_counts_validator fails when counts differ"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["instrument_specifications"] = "RM Young 05103-45 Alpine"
        errors = instrument_counts_validator(ds)
        assert len(errors) == 1
        assert "entries" in errors[0]


def test_instrument_counts_validations_not_measurement():
    """Tests that instrument_counts_validator is skipped for hindcasts"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["data_type"] = "Hindcast"
        errors = instrument_counts_validator(ds)
        assert len(errors) == 0
