import xarray as xr

from ..validators.variables.varinterval_validator import (
    _check_randomly_selected_intervals_min_max,  # type: ignore
    none_larger_than_max_validator,
    none_less_than_min_validator,
)
from .test_sig_digs import test_config


def test_minimum_rounds_off_compression_noise():
    with xr.open_mfdataset("examples/hindcast_example/*.nc") as ds:
        test_config.min = 856.55  # dummy "expected" min
        test_config.max = 1143.65  # dummy "expected" max
        test_config.number_of_significant_decimals = 2
        ds["P"][  # pylint: disable=unsupported-assignment-operation
            0, 0, 0, 1
        ] = 856.5485
        ds["P"][  # pylint: disable=unsupported-assignment-operation
            0, 0, 0, 0
        ] = 1143.6545
        data_array = ds["P"]

        errors = none_less_than_min_validator(data_array, test_config)
        errors += none_larger_than_max_validator(data_array, test_config)

        assert len(errors) == 0


def test_over_max_interval():
    with xr.open_mfdataset("examples/hindcast_example/*.nc") as ds:
        test_config.min = -99999  # dummy "expected" max
        test_config.max = 1
        ds["P"][:, 1, 0, 4] = 2  # pylint: disable=unsupported-assignment-operation
        data_array = ds["P"]

        dims = ["Time", "height_P", "south_north", "west_east"]
        errors = _check_randomly_selected_intervals_min_max(
            data_array, test_config, dims
        )  # type: ignore
        assert len(errors) == 1
        assert "overmax" in errors[0]


def test_under_min_interval():
    with xr.open_mfdataset("examples/hindcast_example/*.nc") as ds:
        test_config.min = 0  # dummy "expected" max
        test_config.max = 9999999
        ds["P"][:, 2, 3, 2] = -1  # pylint: disable=unsupported-assignment-operation
        data_array = ds["P"]

        dims = ["Time", "height_P", "south_north", "west_east"]
        errors = _check_randomly_selected_intervals_min_max(
            data_array, test_config, dims
        )  # type: ignore
        assert len(errors) == 1
        assert "undermin" in errors[0]
