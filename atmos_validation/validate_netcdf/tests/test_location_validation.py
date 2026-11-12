import xarray as xr

from ..validators.file_attributes import location_validator


def test_location_validations_ok():
    """Tests that location_validator passes for the new "<lat>N <lon>E, <datum>" notation"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        for value in ["60.3589N 70.8764E, WGS84", "-60.3589N -70.8764E, ED50"]:
            ds.attrs["location"] = value
            errors = location_validator(ds)
            assert len(errors) == 0


def test_location_validations_old_notation_rejected():
    """Tests that location_validator rejects the old "°N/S ... °E/W" notation"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["location"] = "32.8826°N 63.9245°W, WGS84"
        errors = location_validator(ds)
        assert len(errors) == 1
        assert "does not match the required notation" in errors[0]


def test_location_validations_disallowed_datum():
    """Tests that location_validator rejects a datum not in the allowed list"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["location"] = "60.3589N 70.8764E, WGS-84"
        errors = location_validator(ds)
        assert len(errors) == 1
        assert "not in the allowed list" in errors[0]


def test_location_validations_both_wrong():
    """Tests that location_validator reports both a notation and a datum error together"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["location"] = "32.8826°N 63.9245°W, WGS-84"
        errors = location_validator(ds)
        assert len(errors) == 2
