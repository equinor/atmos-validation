from importlib import import_module

import pytest

from atmos_validation.schemas import Contractor
from atmos_validation.validate_ascii import validate_contractor_header
from atmos_validation.validate_ascii.header_parser import HeaderParser

ascii_main = import_module("atmos_validation.validate_ascii.main")


def test_ascii_contractor_and_multiple_divisions_pass(monkeypatch):
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

    assert errors == []


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


def test_ascii_na_division_is_not_validated_as_a_division(monkeypatch):
    monkeypatch.setattr(
        ascii_main,
        "load_contractor_configs",
        lambda: [Contractor(contractor="Oceanweather Inc.", divisions=None)],
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


def test_ascii_division_may_belong_to_any_selected_contractor(monkeypatch):
    monkeypatch.setattr(
        ascii_main,
        "load_contractor_configs",
        lambda: [
            Contractor(contractor="Oceanweather Inc.", divisions=["Marine"]),
            Contractor(contractor="Example Contractor", divisions=["Offshore"]),
        ],
    )

    errors = validate_contractor_header(
        "Oceanweather Inc., Example Contractor", "Marine, Offshore, Marine"
    )

    assert errors == []


def test_contractor_division_header_is_optional():
    errors = []

    value = HeaderParser([]).get_simple_value(
        "Contractor Division", errors, optional=True
    )

    assert value == ""
    assert errors == []
