from importlib import import_module

import pytest

from atmos_validation.schemas import Contractor
from atmos_validation.validate_ascii import validate_contractor_header
from atmos_validation.validate_ascii.header_parser import HeaderParser

ascii_main = import_module("atmos_validation.validate_ascii.main")


def test_ascii_contractor_and_multiple_divisions_are_rejected(monkeypatch):
    monkeypatch.setattr(
        ascii_main,
        "load_contractor_configs",
        lambda: [
            Contractor(
                contractor="Oceanweather Inc.",
                divisions=["Marine", "Offshore", "Wind", "Wave", "Current"],
            )
        ],
    )

    errors = validate_contractor_header(
        "Oceanweather Inc.", "Marine, Offshore, Wind, Wave, Current"
    )

    assert len(errors) == 1
    assert "same length" in errors[0]


def test_ascii_unknown_contractor_is_rejected(monkeypatch):
    monkeypatch.setattr(
        ascii_main,
        "load_contractor_configs",
        lambda: [Contractor(contractor="Oceanweather Inc.", divisions=["Marine"])],
    )

    errors = validate_contractor_header("Unknown Contractor", "")

    assert len(errors) == 1
    assert "Unknown Contractor" in errors[0]


@pytest.mark.parametrize("division", ["NA", "Marine"])
def test_ascii_na_contractor_means_no_contractor(monkeypatch, division):
    monkeypatch.setattr(
        ascii_main,
        "load_contractor_configs",
        lambda: [Contractor(contractor="Oceanweather Inc.", divisions=["Marine"])],
    )

    errors = validate_contractor_header("NA", division)

    if division == "Marine":
        assert len(errors) == 1
        assert 'Division "Marine"' in errors[0]
    else:
        assert errors == []


@pytest.mark.parametrize("configured_divisions", [None, [], ["Marine"]])
def test_ascii_na_division_is_not_validated_as_a_division(
    monkeypatch, configured_divisions
):
    monkeypatch.setattr(
        ascii_main,
        "load_contractor_configs",
        lambda: [
            Contractor(contractor="Oceanweather Inc.", divisions=configured_divisions)
        ],
    )

    assert validate_contractor_header("Oceanweather Inc.", "NA") == []


def test_ascii_division_not_allowed_by_selected_contractor_is_rejected(monkeypatch):
    monkeypatch.setattr(
        ascii_main,
        "load_contractor_configs",
        lambda: [
            Contractor(contractor="Oceanweather Inc.", divisions=["Marine"]),
            Contractor(contractor="Example Contractor", divisions=None),
        ],
    )

    errors = validate_contractor_header("Example Contractor", "Marine")

    assert len(errors) == 1
    assert "Marine" in errors[0]


@pytest.mark.parametrize(
    ("divisions", "error_count"),
    [
        ("Marine, Offshore", 0),
        ("Marine, NA", 0),
        ("NA, Offshore", 0),
        ("NA, NA", 0),
        ("", 0),
        ("Offshore, Marine", 2),
        ("Marine", 1),
        ("NA", 1),
        ("Marine, Offshore, Marine", 1),
    ],
)
def test_ascii_divisions_match_contractors_by_position(
    monkeypatch, divisions, error_count
):
    monkeypatch.setattr(
        ascii_main,
        "load_contractor_configs",
        lambda: [
            Contractor(contractor="Oceanweather Inc.", divisions=["Marine"]),
            Contractor(contractor="Example Contractor", divisions=["Offshore"]),
        ],
    )

    errors = validate_contractor_header(
        "Oceanweather Inc., Example Contractor", divisions
    )

    assert len(errors) == error_count
    if divisions == "Offshore, Marine":
        assert 'contractor "Oceanweather Inc."' in errors[0]
        assert 'contractor "Example Contractor"' in errors[1]


def test_contractor_division_header_is_optional():
    errors = []

    value = HeaderParser([]).get_simple_value(
        "Contractor Division", errors, optional=True
    )

    assert value == ""
    assert errors == []
