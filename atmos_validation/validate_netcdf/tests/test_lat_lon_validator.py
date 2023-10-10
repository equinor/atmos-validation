import xarray as xr

from ..validators.dims.spatial_validators import mandatory_attrs_lat_lon_validator


def test_mandatory_attrs_lat_lon_validator_ok():
    """Tests that the lat lon validator passes when LAT and LON have the correct attributes"""
    ds = xr.open_dataset("examples/example_netcdf_measurement.nc")
    ds["LAT"].attrs["long_name"] = "Latitude"
    ds["LAT"].attrs["short_name"] = "Latitude"
    ds["LAT"].attrs["description"] = "Latitude"
    ds["LAT"].attrs["CF_standard_name"] = "latitude"
    ds["LAT"].attrs["units"] = "degree_north"
    ds["LON"].attrs["long_name"] = "Longitude"
    ds["LON"].attrs["short_name"] = "Longitude"
    ds["LON"].attrs["description"] = "Longitude"
    ds["LON"].attrs["CF_standard_name"] = "longitude"
    ds["LON"].attrs["units"] = "degree_east"
    errors = mandatory_attrs_lat_lon_validator(ds)
    assert len(errors) == 0
    ds.close()


def test_mandatory_attrs_lat_lon_validator_not_ok():
    """Tests that the lat lon validator reports errors on incorrect attributes"""
    ds = xr.open_dataset("examples/example_netcdf_measurement.nc")
    del ds["LAT"].attrs["long_name"]  # error 0
    ds["LAT"].attrs["short_name"] = "Latitude"
    ds["LAT"].attrs["description"] = "Latitude"
    ds["LAT"].attrs["CF_standard_name"] = "latitude"
    ds["LAT"].attrs["units"] = "degree_north"
    ds["LON"].attrs["long_name"] = "Longitude"
    ds["LON"].attrs["short_name"] = "longiturd"  # error 1
    ds["LON"].attrs["description"] = "Longitude"
    ds["LON"].attrs["CF_standard_name"] = "longitude"
    ds["LON"].attrs["units"] = "degrees"  # error 2
    errors = mandatory_attrs_lat_lon_validator(ds)
    assert len(errors) == 3
    assert "long_name" in errors[0]
    assert "longiturd" in errors[1]
    assert "degrees" in errors[2]
    ds.close()
