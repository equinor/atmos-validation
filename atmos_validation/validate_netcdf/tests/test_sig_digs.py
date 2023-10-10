import xarray as xr

from ...schemas import ParameterConfig
from ..validators.variables.sig_dig_validator import sig_dig_validator

test_config = ParameterConfig(
    key="P",
    long_name="test",
    short_name="test",
    description="test",
    allowed_instruments=[],
    number_of_significant_decimals=10,  # force errors
    parameter_category="test",
    parameter_type="test",
    units="test",
    min=0,
    max=10,
    CF_standard_name="test",
    dims=["Time", "height_P", "south_north", "west_east"],
)


def test_sig_digs_with_errors():
    ds = xr.open_dataset("examples/example_netcdf_measurement.nc")
    errors = sig_dig_validator(ds["WD"], test_config, number_of_iterations=10)
    assert len(errors) == 1
    assert "10/10" in errors[0]
    ds.close()


def test_sig_digs_no_errors():
    ds = xr.open_dataset("examples/example_netcdf_measurement.nc")
    test_config.number_of_significant_decimals = 2
    errors = sig_dig_validator(ds["WS"], test_config, number_of_iterations=10)
    assert len(errors) == 0
    ds.close()
