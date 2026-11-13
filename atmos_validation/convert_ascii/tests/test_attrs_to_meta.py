import numpy as np
import pytest
import xarray as xr

from atmos_validation.convert_ascii import attrs_to_meta
from atmos_validation.convert_ascii.df_to_nc import assign_metadata_to_ds
from atmos_validation.convert_ascii.utils import store_netcdf


@pytest.mark.parametrize(
    ("contractor", "division", "expected_contractors", "expected_divisions"),
    [
        ("Oceanweather Inc.", "Marine", ["Oceanweather Inc."], ["Marine"]),
        ("NA", "NA", ["NA"], ["NA"]),
        ("Fugro, RPS", "Fugro GB Ltd., NA", ["Fugro", "RPS"], ["Fugro GB Ltd.", "NA"]),
        (
            "Fugro, RPS",
            "NA, RPS Group Inc.",
            ["Fugro", "RPS"],
            ["NA", "RPS Group Inc."],
        ),
        ("Fugro, RPS", "NA, NA", ["Fugro", "RPS"], ["NA", "NA"]),
        ("Fugro, RPS", "", ["Fugro", "RPS"], []),
        ("Fugro, RPS", None, ["Fugro", "RPS"], []),
    ],
)
def test_ascii_contractors_are_converted_to_lists(
    tmp_path,
    monkeypatch,
    contractor,
    division,
    expected_contractors,
    expected_divisions,
):
    attrs_map = {
        "comments": "Comments",
        "contractor": "Contractor/Data Responsible",
        "contractor_division": "Contractor Division",
        "data_history": "History",
        "final_reports": "Final reports",
        "project_name": "Project",
        "qc_provider": "QC provider",
        "averaging_period": "Averaging period",
        "data_usability": "Data usability",
        "instrument_types": "Instrument types",
        "instrument_specifications": "Instrument specifications",
        "installation_type": "Installation type",
        "country": "Country",
        "location": "Location",
        "mooring_name": "Mooring name",
        "total_water_depth": "Total water depth",
    }
    monkeypatch.setattr(attrs_to_meta, "get_encoding", lambda _: "utf-8")
    monkeypatch.setattr(attrs_to_meta, "load_attrs_map", lambda _: attrs_map)
    source = tmp_path / "measurement.txt"
    source.write_text(
        "\n".join(
            [
                "% Comments: processed",
                f"% Contractor/Data Responsible: {contractor}",
                *(
                    [f"% Contractor Division: {division}"]
                    if division is not None
                    else []
                ),
                "% History: Original data",
                "% Final reports: NA",
                "% Project: Example",
                "% QC provider: Example QC",
                "% Averaging period: 10 min",
                "% Data usability: usable",
                "% Instrument types: sensor",
                "% Instrument specifications: specification",
                "% Installation type: fixed",
                "% Country: NO",
                "% Location: North Sea",
                "% Mooring name: Example",
                "% Total water depth: 100 m",
            ]
        ),
        encoding="utf-8",
    )

    metadata = attrs_to_meta.parse_measurement_attrs(str(source), "unused")

    assert metadata.contractor == expected_contractors
    assert metadata.contractor_division == expected_divisions

    ds = xr.Dataset(coords={"Time": [np.datetime64("2026-01-01", "ns")]})
    assign_metadata_to_ds(str(source), ds)
    assert ds.attrs["contractor"] == expected_contractors
    assert ds.attrs["contractor_division"] == expected_divisions

    path = store_netcdf(str(source), ds)
    with xr.open_dataset(path, engine="h5netcdf") as reopened:
        for key, expected in (
            ("contractor", expected_contractors),
            ("contractor_division", expected_divisions),
        ):
            actual = reopened.attrs[key]
            assert ([actual] if isinstance(actual, str) else list(actual)) == expected
