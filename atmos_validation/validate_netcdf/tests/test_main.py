import os
from unittest.mock import MagicMock

import xarray as xr

from atmos_validation.validate_netcdf import validation_settings

from ..main import validate
from ..validation_logger import log, setup_logger
from ..validators.root_validator import ValidationResult

PATH_TO_DUMMY_DATASET = os.path.relpath(
    os.path.join(os.curdir, "api", "dev_storage", "dummy_data")
)

HINDCAST_EXAMPLE_DIR = "examples/hindcast_example"


def test_validate():
    """Launch validation using local dummy set for development, testing and debugging"""
    result = validate(PATH_TO_DUMMY_DATASET)
    assert isinstance(result, ValidationResult)


def test_inject_log():
    """Test that the injected log is the one written to"""
    _log = setup_logger(write_to_file=False)
    _log.debug = MagicMock()
    validate(PATH_TO_DUMMY_DATASET, _log)

    expected = (
        "this should be a mocked debug call, we are simply testing "
        "that the import from the module passes it through to to underlying logging object"
    )
    log.debug(expected)
    # ignore type as typechecker does not understand that this should be a mock
    log.debug.assert_called_with(expected)  # type:ignore


def test_multi_year():
    """Use a file that contains more than one year e.g measurements"""
    path_to_multi_year = os.path.relpath(
        os.path.join(
            os.curdir,
            "examples/example_netcdf_measurement.nc",
        )
    )

    result = validate(path_to_multi_year)
    if isinstance(result, ValidationResult):
        assert not any("example_measurement.nc" in error for error in result.errors)


def test_skip_warnings():
    validate(
        path="examples/hindcast_example",
        additional_args=[validation_settings.SKIP_WARNINGS],
    )
    # cleanup
    validation_settings.SETTINGS.remove(validation_settings.SKIP_WARNINGS)


def test_conflicting_coordinates_across_files(tmp_path):
    """A shifted (but same-shape) grid in one file must be reported, not
    silently discarded in favour of the first file's coordinates."""
    files = sorted(f for f in os.listdir(HINDCAST_EXAMPLE_DIR) if f.endswith(".nc"))
    for i, filename in enumerate(files):
        ds = xr.open_dataset(
            os.path.join(HINDCAST_EXAMPLE_DIR, filename), engine="h5netcdf"
        ).load()
        if i == 1:
            ds["LON"] = ds["LON"] + 0.5
        ds.to_netcdf(tmp_path / filename, engine="h5netcdf")
        ds.close()

    result = validate(str(tmp_path))

    assert any("Conflicting static coordinates" in error for error in result.errors)
