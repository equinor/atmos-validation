import re
from typing import List

from .utils import trim_value


class HeaderPosition:
    def __init__(self, position_text: str):
        self.parse_location(self.replace_special_character(position_text))

    def parse_location(self, location_text: str):
        match = None
        regex_example = (
            "location should match e.g 11.574483°N 108.36825°E, WGS84 or "
            "11.574483°S 108.36825°W, some123 ranD0m characters"
        )
        pattern = re.compile(
            r"^[0-9]*\.[0-9]+°[NS] [0-9]*\.[0-9]+°[EW],.+$", re.IGNORECASE
        )
        match = pattern.match(location_text)
        if match is None:
            raise ValueError(
                f"the location string {location_text} should match the regex {pattern.pattern}. "
                f"valid examples: {regex_example}"
            )
        try:
            items = location_text.split(",")
            location_items = items[0].split(" ")
            self.location_text = location_text
            self.latitude = trim_value(location_items[0])
            self.longitude = trim_value(location_items[1])
            self.datum = trim_value(items[1])
        except Exception as e:
            print(e)

    def get_latitude(self) -> str:
        return self.get_position_value(self.latitude, "S")

    def get_longitude(self) -> str:
        return self.get_position_value(self.longitude, "W")

    def get_position_value(self, text_in: str, direction: str) -> str:
        index = text_in.find("°")
        value = text_in[0:index]
        if text_in[index + 1 : len(text_in)] == direction:
            return "-" + self.replace_special_character(value)
        return self.replace_special_character(value)

    def replace_special_character(self, text_in: str) -> str:
        return text_in.replace("�", "°").replace("Â", "°")

    def validate(self) -> List[str]:
        messages = []
        try:
            messages = messages + self.validate_latitude()
            messages = messages + self.validate_longitude()
        except Exception:
            messages.append("Location could not be parsed")
        return messages

    def validate_latitude(self) -> List[str]:
        return self.validate_item(self.get_latitude(), "Latitude", -90, 90)

    def validate_longitude(self) -> List[str]:
        return self.validate_item(self.get_longitude(), "Longitude", -180, 180)

    def validate_item(
        self, value: str, position: str, lower: int, upper: int
    ) -> List[str]:
        messages = []
        if len(value) == 0:
            messages.append(position + " could not be parsed")
        value_f = float(value)
        if value_f < lower or value_f > upper:
            messages.append(position + " should be between +-90")
        return messages
