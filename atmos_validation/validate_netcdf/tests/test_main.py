import os
from unittest.mock import MagicMock

from atmos_validation.validate_netcdf import validation_settings

from ..main import validate
from ..validation_logger import log, setup_logger
from ..validators.root_validator import ValidationResult

PATH_TO_DUMMY_DATASET = os.path.relpath(
    os.path.join(os.curdir, "api", "dev_storage", "dummy_data")
)


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
