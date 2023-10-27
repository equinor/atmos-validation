import xarray as xr

from ...schemas.classification_level import ClassificationLevel
from ..validators.file_attributes import classification_level_validator


def test_classification_level_not_ok():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["classification_level"] = "Not Allowed"
        errors = classification_level_validator(ds)
        assert len(errors) == 1
        assert str(list(ClassificationLevel)) in errors[0]


def test_classification_level_ok():
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["classification_level"] = ClassificationLevel.OPEN
        errors = classification_level_validator(ds)
        assert len(errors) == 0
