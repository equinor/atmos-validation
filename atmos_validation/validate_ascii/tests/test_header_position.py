import pytest

from ..header_position import HeaderPosition


def test_header_position_ok_north_east():
    """Tests that a north-east location with an allowed datum parses and validates cleanly"""
    position = HeaderPosition("60.3589N 70.8764E, WGS84")
    assert position.get_latitude() == "60.3589"
    assert position.get_longitude() == "70.8764"
    assert position.datum == "WGS84"
    assert position.validate() == []


def test_header_position_ok_south_west():
    """Tests that a south-west location (negative sign, fixed N/E letters) parses and validates cleanly"""
    position = HeaderPosition("-60.3589N -70.8764E, ED50")
    assert position.get_latitude() == "-60.3589"
    assert position.get_longitude() == "-70.8764"
    assert position.datum == "ED50"
    assert position.validate() == []


def test_header_position_old_notation_rejected():
    """Tests that the old "°N/S ... °E/W" notation is no longer accepted"""
    with pytest.raises(ValueError):
        HeaderPosition("32.8826°N 63.9245°W, WGS84")


def test_header_position_disallowed_datum():
    """Tests that a datum outside the allowed list is reported by validate()"""
    position = HeaderPosition("60.3589N 70.8764E, WGS-84")
    errors = position.validate()
    assert len(errors) == 1
    assert "not in the allowed list" in errors[0]


def test_header_position_out_of_range_latitude():
    """Tests that an out-of-range latitude is reported by validate()"""
    position = HeaderPosition("95.0000N 70.8764E, WGS84")
    errors = position.validate()
    assert any("Latitude should be between" in error for error in errors)
