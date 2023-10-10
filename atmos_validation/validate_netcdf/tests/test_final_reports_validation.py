import xarray as xr

from ..validators.file_attributes import final_reports_validator

PATH_TO_TEST_DATA = "examples/example_netcdf_measurement.nc"


def test_final_reports_ok():
    """Tests when final_reports is valid (a lists of string)"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = ["foo", "bar"]
        errors = final_reports_validator(ds)
        assert len(errors) == 0


def test_final_reports_empty_list_ok():
    """Tests when final_reports is valid (and empty list)"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = []
        errors = final_reports_validator(ds)
        assert len(errors) == 0


def test_final_reports_not_list_not_ok():
    """Tests when final_reports is not valid (not a lists of string)"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = "this should be a list of strings"
        errors = final_reports_validator(ds)
        assert len(errors) == 1
        assert "must be a list of strings" in errors[0]


def test_final_reports_list_of_non_strings_not_ok():
    """Tests when final_reports is not valid (a lists of not all string)"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = ["this should be a list of strings", 3.14]
        errors = final_reports_validator(ds)
        assert len(errors) == 1
        assert "must be a list of strings" in errors[0]
