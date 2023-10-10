from dataclasses import dataclass
from typing import List, Optional

from .header_date import HeaderDate
from .header_names import Headers
from .header_parameter_info_list import HeaderParameterInfoList
from .header_position import HeaderPosition


@dataclass
# pylint: disable=too-many-instance-attributes
class HeaderMetaData:
    number_of_header_lines: int
    contractor: str
    final_report: str
    qc: str
    duration: HeaderDate
    mooring_name: str
    position: HeaderPosition
    water_depth: str
    instruments: str
    data_usability_level: str
    data_history: str
    project: str
    averaging_period: str
    installation_type: str
    instrument_spec: str
    parameters: HeaderParameterInfoList
    empty_value: str
    comments: str

    def is_minute_based(self) -> bool:
        attr = (info.key for info in self.parameters.filter_items(False))
        return "Min" in attr

    def mandatory(self, value: str, prefix: str):
        messages = []
        if self.is_string_empty(value):
            messages.append(prefix + " mandatory")
        if value == "NA":
            messages.append(prefix + " mandatory")
        return messages

    def validate_empty_value(self) -> List[str]:
        messages = []
        if not self.is_string_empty(self.empty_value):
            items = self.empty_value.split(",")
            if len(items) > 1:
                messages.append(Headers.NULL_VALUE + " should only have 1 item")
        return messages

    def is_string_empty(self, value: Optional[str]) -> bool:
        return value is None or value == ""

    def validate(self) -> List[str]:
        """Requires a callable that can check the existence of a file based on a path string"""
        messages: List[str] = []
        messages += self.mandatory(self.mooring_name, Headers.MOORING)
        messages += self.validate_empty_value()
        self.validate_instrument_spec(messages)
        messages += self.duration.validate()
        messages += self.position.validate()
        messages += self.validate_comment_length()
        messages += self.parameters.validate()
        return messages

    def validate_instrument_spec(self, messages: List[str]):
        if self.instrument_spec.strip().upper() != "NA" and self.instruments.count(
            ","
        ) != self.instrument_spec.count(","):
            messages.append(
                "Different numbers of comma separated items in instruments and instruments spec for metadata header"
            )

    def validate_comment_length(self) -> List[str]:
        if len(self.comments) > 599:
            return ["Max comment length is 600 characters"]
        return []
