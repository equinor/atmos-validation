from pytest import raises

from .. import (
    DataUsabilityLevel,
    DataUsabilityLevels,
    InstallationType,
    InstallationTypes,
    InstrumentType,
    InstrumentTypes,
)


def test_require_unique_data_usability_levels():
    with raises(ValueError):
        DataUsabilityLevels(
            configs=[
                DataUsabilityLevel(level="duplicate"),
                DataUsabilityLevel(level="duplicate"),
            ]
        )


def test_require_unique_instrument_types():
    with raises(ValueError):
        InstrumentTypes(
            configs=[
                InstrumentType(instrument_type="duplicate"),
                InstrumentType(instrument_type="duplicate"),
            ]
        )


def test_unique_instrument_types_ok():
    InstrumentTypes(
        configs=[
            InstrumentType(instrument_type="unique1"),
            InstrumentType(instrument_type="unique2"),
        ]
    )


def test_require_unique_installation_types():
    with raises(ValueError):
        InstallationTypes(
            configs=[
                InstallationType(installation_type="duplicate"),
                InstallationType(installation_type="duplicate"),
            ]
        )
