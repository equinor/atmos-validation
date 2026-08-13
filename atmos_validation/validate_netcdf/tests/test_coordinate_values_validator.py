import numpy as np
import xarray as xr

from ..validators.dims.spatial_validators import coordinate_values_validator


def test_valid_coordinates_pass():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        assert coordinate_values_validator(ds) == []


def test_lat_out_of_range_reported():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["LAT"].values[:] = 91.0
        errors = coordinate_values_validator(ds)
        assert len(errors) == 1
        assert "LAT" in errors[0]
        assert "[-90.0, 90.0]" in errors[0]


def test_lon_out_of_range_reported():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["LON"].values[:] = -181.0
        errors = coordinate_values_validator(ds)
        assert len(errors) == 1
        assert "LON" in errors[0]


def test_non_finite_lat_reported():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds["LAT"].values[:] = np.nan
        errors = coordinate_values_validator(ds)
        assert any("non-finite" in error and "LAT" in error for error in errors)


def test_non_finite_height_reported():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        length = ds.sizes["height_WD"]
        ds = ds.assign_coords(height_WD=("height_WD", np.full(length, np.inf)))
        errors = coordinate_values_validator(ds)
        assert any("non-finite" in error and "height_WD" in error for error in errors)


def test_missing_lat_lon_not_reported_here():
    errors = coordinate_values_validator(xr.Dataset())
    assert errors == []
