import logging

import pytest
import requests
import xarray as xr

from ..validation_settings import (
    URL_TO_CONTRACTORS,
    URL_TO_DATA_USABILITY,
    URL_TO_INST_TYPES,
)
from ..validators.file_attributes import (
    contractors_validator,
    file_attributes_validator,
)


def _mock_contractor_config(monkeypatch):
    monkeypatch.setattr(
        "atmos_validation.validate_netcdf.validators.file_attributes.fetch_config_bytes",
        lambda _: (
            b'[{"contractor":"Oceanweather Inc.","divisions":'
            b'["Marine","Offshore","Wind","Wave","Current"]},'
            b'{"contractor":"Example Contractor","divisions":null}]'
        ),
    )


def test_contractor_must_be_in_configuration(monkeypatch):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(attrs={"contractor": ["Unknown Contractor"]})

    errors = contractors_validator(ds)

    assert len(errors) == 1
    assert "Unknown Contractor" in errors[0]


def test_configured_contractors_pass(monkeypatch):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(attrs={"contractor": ["Oceanweather Inc."]})

    assert contractors_validator(ds) == []


@pytest.mark.parametrize("contractor", [[], "NA", ["NA"]])
@pytest.mark.parametrize("division", [[], "NA", "Marine"])
def test_no_contractor_representations_are_equivalent(
    monkeypatch, contractor, division
):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(attrs={"contractor": contractor, "contractor_division": division})

    errors = contractors_validator(ds)

    if division == "Marine":
        assert len(errors) == 1
        assert 'Division "Marine"' in errors[0]
    else:
        assert errors == []


def test_contractor_as_string_is_validated(monkeypatch):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(attrs={"contractor": "Unknown Contractor"})

    errors = contractors_validator(ds)

    assert len(errors) == 1
    assert "Unknown Contractor" in errors[0]


def test_multiple_divisions_are_validated_against_selected_contractors(monkeypatch):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(
        attrs={
            "contractor": ["Oceanweather Inc.", "Example Contractor"],
            "contractor_division": ["Marine", "Aviation"],
        }
    )

    errors = contractors_validator(ds)

    assert len(errors) == 1
    assert "Aviation" in errors[0]
    assert "not allowed" in errors[0]


def test_null_divisions_do_not_allow_any_division(monkeypatch):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(
        attrs={
            "contractor": ["Example Contractor"],
            "contractor_division": ["Marine"],
        }
    )

    errors = contractors_validator(ds)

    assert len(errors) == 1
    assert "Marine" in errors[0]


def test_valid_multiple_divisions_pass(monkeypatch):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(
        attrs={
            "contractor": ["Oceanweather Inc."],
            "contractor_division": ["Marine", "Offshore", "Wind", "Wave", "Current"],
        }
    )

    assert contractors_validator(ds) == []


def test_divisions_may_belong_to_any_selected_contractor(monkeypatch):
    monkeypatch.setattr(
        "atmos_validation.validate_netcdf.validators.file_attributes.fetch_config_bytes",
        lambda _: (
            b'[{"contractor":"Oceanweather Inc.","divisions":["Marine"]},'
            b'{"contractor":"Example Contractor","divisions":["Offshore"]}]'
        ),
    )
    ds = xr.Dataset(
        attrs={
            "contractor": ["Oceanweather Inc.", "Example Contractor"],
            "contractor_division": ["Offshore", "Marine", "Offshore"],
        }
    )

    assert contractors_validator(ds) == []


@pytest.mark.parametrize("division", ["Marine", "Aviation"])
def test_string_contractor_and_division_are_validated(monkeypatch, division):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(
        attrs={"contractor": "Oceanweather Inc.", "contractor_division": division}
    )

    errors = contractors_validator(ds)

    if division == "Marine":
        assert errors == []
    else:
        assert len(errors) == 1
        assert "Aviation" in errors[0]


@pytest.mark.parametrize(
    "divisions",
    [
        ["Marine", "Offshore", "Wind", "Wave", "Current"],
        ["Aviation"],
    ],
)
def test_divisions_are_validated_after_netcdf_round_trip(
    monkeypatch, tmp_path, divisions
):
    _mock_contractor_config(monkeypatch)
    ds = xr.Dataset(
        attrs={
            "contractor": ["Oceanweather Inc."],
            "contractor_division": divisions,
        }
    )
    path = tmp_path / "contractors.nc"
    ds.to_netcdf(path, engine="h5netcdf")

    with xr.open_dataset(path, engine="h5netcdf") as reopened:
        errors = contractors_validator(reopened)

    if divisions == ["Aviation"]:
        assert len(errors) == 1
        assert "Aviation" in errors[0]
    else:
        assert errors == []


def test_file_attributes_validator_reports_invalid_division(monkeypatch):
    configs = {
        URL_TO_CONTRACTORS: (
            b'[{"contractor":"Oceanweather Inc.","divisions":["Marine"]}]'
        ),
        URL_TO_INST_TYPES: b'[{"installation_type":"Platform"}]',
        URL_TO_DATA_USABILITY: b'[{"level":"Processed"}]',
    }
    monkeypatch.setattr(
        "atmos_validation.validate_netcdf.validators.file_attributes.fetch_config_bytes",
        configs.__getitem__,
    )
    with xr.open_dataset("examples/example_netcdf_measurement.nc") as ds:
        ds.attrs["contractor"] = "Oceanweather Inc."
        ds.attrs["contractor_division"] = "Aviation"

        errors = file_attributes_validator(ds)

    contractor_errors = [error for error in errors if ":contractors:" in error]
    assert len(contractor_errors) == 1
    assert "Aviation" in contractor_errors[0]
    assert "not allowed" in contractor_errors[0]


def test_contractor_config_download_failure_is_reported(monkeypatch):
    def fail_download(_):
        raise requests.ConnectionError("Contractor configuration unavailable")

    monkeypatch.setattr(
        "atmos_validation.validate_netcdf.validators.file_attributes.fetch_config_bytes",
        fail_download,
    )
    monkeypatch.setattr(
        "atmos_validation.validate_netcdf.utils.log.error",
        logging.getLogger(__name__).error,
    )
    ds = xr.Dataset(attrs={"contractor": "Oceanweather Inc."})

    errors = contractors_validator(ds)

    assert len(errors) == 1
    assert "Contractor configuration unavailable" in errors[0]
