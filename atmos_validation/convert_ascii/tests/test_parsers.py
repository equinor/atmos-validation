from ..parsers import parse_location_text


def test_parse_location_text_north_east():
    """Tests parsing a north-east location line into signed (lat, lon) floats"""
    lat, lon = parse_location_text("% Location: 60.3589N 70.8764E, WGS84")
    assert lat == 60.3589
    assert lon == 70.8764


def test_parse_location_text_south_west():
    """Tests parsing a south-west location line (negative sign) into signed (lat, lon) floats"""
    lat, lon = parse_location_text("% Location: -60.3589N -70.8764E, WGS84")
    assert lat == -60.3589
    assert lon == -70.8764
