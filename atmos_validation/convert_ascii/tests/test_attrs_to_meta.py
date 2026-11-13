from atmos_validation.convert_ascii import attrs_to_meta


def test_ascii_contractor_is_converted_to_single_item_list(tmp_path, monkeypatch):
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
                "% Contractor/Data Responsible: Oceanweather Inc.",
                "% Contractor Division: Marine",
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

    assert metadata.contractor == ["Oceanweather Inc."]
    assert metadata.contractor_division == ["Marine"]
