import xarray as xr

from ..validators.file_attributes import final_reports_validator

PATH_TO_TEST_DATA = "examples/example_netcdf_measurement.nc"


def test_final_reports_ok():
    """Tests when final_reports is valid (a lists of string with correct extension)"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = ["foo.pdf", "bar.docx"]
        errors = final_reports_validator(ds)
        assert len(errors) == 0


def test_final_reports_empty_list_ok():
    """Tests when final_reports is valid (an empty list)"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = []
        errors = final_reports_validator(ds)
        assert len(errors) == 0


def test_final_reports_empty_string_ok():
    """Tests when final_reports is valid (an empty string)"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = ""
        errors = final_reports_validator(ds)
        assert len(errors) == 0


def test_final_reports_NA_ok():
    """Tests when final_reports is NA"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = "NA"
        errors = final_reports_validator(ds)
        assert len(errors) == 0


def test_final_reports_list_of_non_strings_not_ok():
    """Tests when final_reports is not valid (wrong type in list)"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = ["some_report.pdf", 1]  # wrong type
        errors = final_reports_validator(ds)
        assert len(errors) == 1
        assert "is not comma-separated string or string list" in errors[0]


def test_final_reports_not_string_not_ok():
    """Tests when final_reports is of wrong data type"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = True  # wrong type, should be string
        errors = final_reports_validator(ds)
        assert len(errors) == 1
        assert "is not comma-separated string or string list" in errors[0]


def test_final_reports_list_wrong_file_extension_not_ok():
    """Tests when final_reports string includes non-valid file extensions"""
    with xr.open_dataset(PATH_TO_TEST_DATA) as ds:
        ds.attrs["final_reports"] = "wrong.file_extension, one_more.error"
        errors = final_reports_validator(ds)
        assert len(errors) == 2
        assert "File extension for final_reports" in errors[0]
