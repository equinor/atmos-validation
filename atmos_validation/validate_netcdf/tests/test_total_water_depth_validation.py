import xarray as xr

from ..validators.file_attributes import total_water_depth_validator


def test_total_water_depth_validations_ok():
    """Tests that total_water_depth_validator passes for the allowed unit "m" """
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        errors = total_water_depth_validator(ds)
        assert len(errors) == 0


def test_total_water_depth_validations_na_ok():
    """Tests that total_water_depth_validator allows "NA" for wind data"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["total_water_depth"] = "NA"
        errors = total_water_depth_validator(ds)
        assert len(errors) == 0


def test_total_water_depth_validations_wrong_unit():
    """Tests that total_water_depth_validator fails for a disallowed unit"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["total_water_depth"] = "53.2 ft"
        errors = total_water_depth_validator(ds)
        assert len(errors) == 1
        assert "not allowed" in errors[0]


def test_total_water_depth_validations_missing_unit():
    """Tests that total_water_depth_validator fails when no unit is given"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["total_water_depth"] = "53.2"
        errors = total_water_depth_validator(ds)
        assert len(errors) == 1


def test_total_water_depth_validations_bare_float_missing_unit():
    """Tests that total_water_depth_validator fails for a bare float with no unit"""
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["total_water_depth"] = 53.2
        errors = total_water_depth_validator(ds)
        assert len(errors) == 1
