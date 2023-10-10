from pytest import raises

from .. import ParameterConfig, ParameterConfigs


def test_require_unique_parameter_configs():
    with raises(ValueError):
        ParameterConfigs(
            configs=[
                ParameterConfig(
                    key="duplicate",
                    dims=[],
                    parameter_category="test",
                    parameter_type="test",
                    short_name="test",
                    long_name="test",
                    description="test",
                    allowed_instruments=["test"],
                    number_of_significant_decimals=2,
                    units="test",
                    min=0,
                    max=1,
                    CF_standard_name="test",
                ),
                ParameterConfig(
                    key="duplicate",
                    dims=[],
                    parameter_category="test",
                    parameter_type="test",
                    short_name="test",
                    long_name="test",
                    description="test",
                    allowed_instruments=["test"],
                    number_of_significant_decimals=2,
                    units="test",
                    min=0,
                    max=1,
                    CF_standard_name="test",
                ),
            ]
        )


def test_needs_correct_dims():
    with raises(ValueError):
        ParameterConfig(
            key="duplicate",
            dims=["not", "allowed"],  # triggers error
            parameter_category="test",
            parameter_type="test",
            short_name="test",
            long_name="test",
            description="test",
            allowed_instruments=["test"],
            number_of_significant_decimals=2,
            units="test",
            min=0,
            max=1,
            CF_standard_name="test",
        )
