import re
from typing import List

ALLOWED_DATUMS = [
    "datum uncertain",
    "WGS84",
    "ED50",
    "ED87",
    "ETRS89",
    "Tokyo",
    "NAD27",
]

# Matches "<lat>N <lon>E, <datum>", e.g. "60.3589N 70.8764E, WGS84" or
# "-60.3589N -70.8764E, WGS84". The sign carries the hemisphere; the N/E
# letters are fixed and do not flip to S/W.
LOCATION_PATTERN = re.compile(r"^-?[0-9]+\.[0-9]+N -?[0-9]+\.[0-9]+E,.+$")


class HeaderPosition:
    def __init__(self, position_text: str):
        self.parse_location(position_text)

    def parse_location(self, location_text: str):
        regex_example = (
            "location should match e.g 60.3589N 70.8764E, WGS84 (north-east) or "
            "-60.3589N -70.8764E, WGS84 (south-west)"
        )
        match = LOCATION_PATTERN.match(location_text)
        if match is None:
            raise ValueError(
                f"the location string {location_text} should match the regex "
                f"{LOCATION_PATTERN.pattern}. valid examples: {regex_example}"
            )
        try:
            items = location_text.split(",", 1)
            location_items = items[0].split(" ")
            self.location_text = location_text
            self.latitude = location_items[0][:-1]  # strip trailing "N"
            self.longitude = location_items[1][:-1]  # strip trailing "E"
            self.datum = items[1].strip()
        except Exception as e:
            print(e)

    def get_latitude(self) -> str:
        return self.latitude

    def get_longitude(self) -> str:
        return self.longitude

    def validate(self) -> List[str]:
        messages = []
        try:
            messages = messages + self.validate_latitude()
            messages = messages + self.validate_longitude()
            messages = messages + self.validate_datum()
        except Exception:
            messages.append("Location could not be parsed")
        return messages

    def validate_latitude(self) -> List[str]:
        return self.validate_item(self.get_latitude(), "Latitude", -90, 90)

    def validate_longitude(self) -> List[str]:
        return self.validate_item(self.get_longitude(), "Longitude", -180, 180)

    def validate_datum(self) -> List[str]:
        if self.datum not in ALLOWED_DATUMS:
            return [
                f'Datum "{self.datum}" is not in the allowed list. '
                f"Allowed values: {ALLOWED_DATUMS}"
            ]
        return []

    def validate_item(
        self, value: str, position: str, lower: int, upper: int
    ) -> List[str]:
        messages = []
        if len(value) == 0:
            messages.append(position + " could not be parsed")
        value_f = float(value)
        if value_f < lower or value_f > upper:
            messages.append(f"{position} should be between {lower} and {upper}")
        return messages
