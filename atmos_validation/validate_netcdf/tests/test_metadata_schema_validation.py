import numpy as np
import xarray as xr

from ..validators.file_attributes import metadata_schema_validator


def test_valid_measurement_passes():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        errors = metadata_schema_validator(ds)
        assert errors == []


def test_valid_hindcast_passes():
    with xr.open_dataset(
        "examples/hindcast_example/example_hindcast_20160101_20160131_T744.nc"
    ) as ds:
        errors = metadata_schema_validator(ds)
        assert errors == []


def test_missing_required_attribute_reported():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        del ds.attrs["averaging_period"]
        errors = metadata_schema_validator(ds)
        assert len(errors) == 1
        assert "averaging_period" in errors[0]
        assert "does not exist" in errors[0]


def test_wrong_type_reported():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["contractor"] = 123
        errors = metadata_schema_validator(ds)
        assert len(errors) == 1
        assert "contractor" in errors[0]


def test_numpy_scalars_are_normalized():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["contractor"] = np.str_("Example Contractor")
        errors = metadata_schema_validator(ds)
        assert errors == []


def test_deferred_field_type_error_not_double_reported():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        # final_reports as a comma-string is handled by final_reports_validator,
        # so the schema validator must not report its non-presence type mismatch.
        ds.attrs["final_reports"] = "report.pdf"
        errors = metadata_schema_validator(ds)
        assert errors == []


def test_missing_country_reported_on_measurement():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        del ds.attrs["country"]
        errors = metadata_schema_validator(ds)
        assert len(errors) == 1
        assert "country" in errors[0]
