from typing import Dict, Optional, Set, Tuple

from pydantic import BaseModel

from .header_names import Headers


class HeaderParameterInfo(BaseModel):
    name: str
    key: str
    unit: str = ""
    height: str = ""
    base: str = ""
    value_format: str = "{0,-: str 10}"
    number_of_decimals: int = 2
    instrument: str = ""
    is_time_parameter: bool = False
    instrument_spec: str = "NA"

    def is_system_parameter(self) -> bool:
        return len(self.base) != 0

    @staticmethod
    def get_valid_height(height: str) -> Tuple[bool, Optional[float]]:
        try:
            return (True, float(height))
        except Exception:
            return (True, None) if height in ["", "NA"] else (False, None)

    def get_validated_height_or_raise(self) -> Optional[float]:
        is_valid, height = HeaderParameterInfo.get_valid_height(self.height)
        if not is_valid:
            raise ValueError(f"Height: {self.height} is invalid")
        return height

    @staticmethod
    def are_instruments_in_listed_instruments(
        instrument: str, listed_instruments: Set[str]
    ) -> bool:
        instruments = [i.strip() for i in instrument.upper().split(",")]
        for i in instruments:
            if i not in listed_instruments:
                return False
        return True

    @staticmethod
    def is_instrument_valid(
        instrument: Optional[str], accepted_values: Dict[str, Set[str]]
    ) -> bool:
        if instrument is None:
            return False
        if instrument == "NA":
            return True
        accepted_instruments = accepted_values[Headers.INSTRUMENTS]
        instruments = [i.strip() for i in instrument.upper().split(",")]
        for i in instruments:
            if i not in accepted_instruments:
                return False
        return True
