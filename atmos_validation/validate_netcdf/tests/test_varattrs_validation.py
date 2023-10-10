import xarray as xr

from ..validators.variables.varattrs_validator import var_allowed_instruments_validator


def test_instruments_attributes_validations_ok():
    """
    Tests for measurement that instrument_types and instrument_specifications
    are following the conventions
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["WS"].attrs["instruments"] = str(
            {"PROPELLER, SOME SPEC": [10.0], "PRESSURE SENSOR, SOME SPEC": [100.0]}
        )
        errors = var_allowed_instruments_validator(
            "WS", ds, ["PRESSURE SENSOR", "PROPELLER"]
        )
        assert len(errors) == 0


def test_instruments_attributes_validations_wrong_instrument():
    """
    Tests for measurement that instrument_types and instrument_specifications
    are following the conventions
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["WS"].attrs["instruments"] = str(
            {"PROPELLER, SOME SPEC": [10.0], "PRESSURE SENSOR, SOME SPEC": [100.0]}
        )
        errors = var_allowed_instruments_validator("WS", ds, ["PRESSURE SENSOR", "GPS"])
        assert len(errors) == 1
        assert "wrong instrument_type" in errors[0]


def test_instruments_attributes_validations_no_instrument_types():
    """
    Missing attributes should not be checked in instrument_types validator.
    Checks that if it is missing we return no errors.
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        del ds["WS"].attrs["instruments"]
        errors = var_allowed_instruments_validator("WS", ds, ["NOT VALID"])
        assert len(errors) == 0


def test_instruments_attributes_validations_not_measurement():
    """
    Checks if data_type is hindcast, we get no errors
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["data_type"] = "Hindcast"
        errors = var_allowed_instruments_validator("WS", ds, ["NOT VALID"])
        assert len(errors) == 0


def test_instruments_attributes_validations_not_parseable():
    """
    Checks if "instrument_types" cant be parsed we get an error
    """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["WS"].attrs["instruments"] = "{PROPELLER ANEMOMETER, NA: [10.0]"
        errors = var_allowed_instruments_validator(
            "WS", ds, ["PROPELLER ANEMOMETER", "SONIC ANEMOMETER"]
        )
        assert len(errors) == 1
        assert "parsed as a dict" in errors[0]
