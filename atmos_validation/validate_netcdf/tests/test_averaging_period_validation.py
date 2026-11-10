import xarray as xr

from ..validators.file_attributes import averaging_period_validator


def test_averaging_period_validations_ok():
    """Tests that averaging_period_validator passes for each allowed unit"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        for value in ["10 min", "30 sec", "1 h"]:
            ds.attrs["averaging_period"] = value
            errors = averaging_period_validator(ds)
            assert len(errors) == 0


def test_averaging_period_validations_not_ok():
    """Tests that averaging_period_validator fails for a disallowed unit"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["averaging_period"] = "10 mins"
        errors = averaging_period_validator(ds)
        assert len(errors) == 1
        assert "not in the allowed list" in errors[0]


def test_averaging_period_validations_case_sensitive():
    """Tests that averaging_period_validator rejects wrong-case units (e.g. "Sec", "H")"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        for value in ["10 Sec", "1 H", "10 MIN"]:
            ds.attrs["averaging_period"] = value
            errors = averaging_period_validator(ds)
            assert len(errors) == 1


def test_averaging_period_validations_missing_unit():
    """Tests that averaging_period_validator fails when no unit is given"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["averaging_period"] = "10"
        errors = averaging_period_validator(ds)
        assert len(errors) == 1
