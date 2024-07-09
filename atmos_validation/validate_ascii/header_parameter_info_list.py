from typing import Dict, List, Set

from .header_names import Headers
from .header_parameter_info import HeaderParameterInfo
from .utils import trim_value


class HeaderParameterInfoList:
    prefix = "% "

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        lines: List[str],
        column_headers: str,
        listed_instruments: Set[str],
        accepted_values: Dict[str, Set[str]],
        system_instrument_spec: str,
    ):
        self.lines = [line for line in lines if line.strip() != self.prefix.strip()]
        self.items: List[HeaderParameterInfo] = []
        self.listed_instruments = listed_instruments
        self.accepted_values = accepted_values
        self.column_headers = [
            x.strip() for x in column_headers[len(self.prefix) - 1 :].split()
        ]
        self.system_instrument_spec = system_instrument_spec
        try:
            for line in lines:
                # To be able to split 'Wind speed 90m           WS90m      m/s     90      WS''
                # It must be larger than 2 spaces
                tokens = self.get_tokens(line)
                if len(tokens) == 2:
                    self.items.append(
                        HeaderParameterInfo(
                            name=self.remove_prefix(trim_value(tokens[0])),
                            key=trim_value(tokens[1]),
                            is_time_parameter=True,
                        )
                    )
                else:
                    self.items.append(
                        HeaderParameterInfo(
                            name=self.remove_prefix(trim_value(tokens[0])),
                            key=trim_value(tokens[1]),
                            unit=trim_value(tokens[2]),
                            height=trim_value(tokens[3]),
                            base=trim_value(tokens[4]),
                            instrument=trim_value(tokens[5]),
                            instrument_spec=trim_value(tokens[6]),
                        )
                    )
        except Exception as e:
            print("error while parsing parameter tokens: ", e, flush=True)

    def get_tokens(self, line: str) -> List[str]:
        # To be able to split 'Wind speed 90m           WS90m      m/s     90      WS''
        # It must be larger than 2 spaces
        line = line.replace("%", "", 1)

        if line.find("\t") > 0:
            items = line.split("\t")
        else:
            items = line.split("  ")
        items = [item.strip() for item in items]
        return [token for token in items if len(token) != 0]

    def remove_prefix(self, token: str) -> str:
        return token.replace(self.prefix, "")

    def filter_items(self, is_system_parameter: bool) -> List[HeaderParameterInfo]:
        return list(
            filter(lambda x: x.is_system_parameter() == is_system_parameter, self.items)
        )

    def get_item_for_col(self, col_nr: int) -> HeaderParameterInfo:
        return self.items[col_nr]

    def get_index_for_col(self, col_name: str) -> int:
        return self.column_headers.index(col_name)

    def validate(self) -> List[str]:
        messages = []
        messages.extend(self.validate_column_headers())
        try:
            if len(self.items) == 0:
                messages.append("Parameters could not be parsed")

            for line in self.lines:
                tokens = self.get_tokens(line)
                if len(tokens) == 2:
                    keys = ["YY", "MM", "DD", "HH", "Min"]
                    if tokens[1] not in keys:
                        messages.append(
                            "Wrong date keys, " + tokens[1] + " not supported"
                        )
                elif len(tokens) != 7:
                    messages.append(
                        f"System parameters should consist of name, abbrev, unit, height, base name, instrument and"
                        f"instrument spec. Token {tokens}. Supported separator at least one tab or at least two spaces"
                    )
                else:
                    messages.extend(self.validate_tokens(tokens))
        except Exception as e:
            print(e)
            messages.append("Parameters could not be parsed ex " + str(e))
        return messages

    def validate_column_headers(self) -> List[str]:
        messages = []
        if len(self.column_headers) != len(self.lines) or len(
            self.column_headers
        ) != len(self.items):
            return [
                f"Number of parsed keys in parameters does not correspond to number of column headers parsed headers: "
                f"{self.column_headers}, parsed keys: {[item.key for item in self.items]}"
            ]
        for col_head, item in zip(self.column_headers, self.items):
            if item.key != col_head:
                messages.append(
                    f"Mismatch between column header {col_head} and parameter {item.key}"
                )
        return messages

    def all_instrumentspecs_in_system(self, param_spec: str, system_spec: str):
        system_specs = set((x.strip() for x in system_spec.upper().split(",")))
        param_specs = (x.strip() for x in param_spec.upper().split(","))
        for spec in param_specs:
            if spec != "NA" and spec not in system_specs:
                return False
        return True

    # Validates the individual parts of the parameter definition, e.g are units permissible?
    def validate_tokens(self, tokens: List[str]) -> List[str]:
        errors = []
        param = tokens[0]
        abbrev = tokens[1]
        unit = tokens[2]
        height = tokens[3]
        base = tokens[4]
        instrument = tokens[5]
        max_abbreviation_length = 25
        max_instrument_spec_length = 250
        max_unit_length = 20
        max_base_length = 20
        instrument_spec = tokens[6]
        if len(base) > max_base_length:
            errors.append(
                f"The base key {base} for param {param} has too many characters. "
                f"It should be no more than {max_base_length} characters long."
            )
        if len(unit) > max_unit_length:
            errors.append(
                f"The unit {unit} for parameter {param} has too many characters. "
                f"It should be max {max_unit_length} characters long."
            )
        if not instrument_spec.strip().upper() == "NA" and instrument.count(
            ","
        ) != instrument_spec.count(","):
            errors.append(
                f"instrument {instrument} and instrument spec: {instrument_spec} "
                f"have different numbers of comma separated elements"
            )
        if not self.all_instrumentspecs_in_system(
            instrument_spec, self.system_instrument_spec
        ):
            errors.append(
                f"The instrument spec {instrument_spec} for parameter {param} does not correlate with what "
                f"is listed in header ({self.system_instrument_spec}). One or more spec could not be found in header"
            )
        if len(instrument_spec) > max_instrument_spec_length:
            errors.append(
                f"The instrument spec {instrument_spec} is too long for the parameter {param}. "
                f"Specs should be less than {max_instrument_spec_length} characters"
            )
        if len(abbrev) > max_abbreviation_length:
            errors.append(
                f"The abbreviated parameter name {abbrev} is too long for the parameter {param}. "
                f"Abbreviations should be less than {max_abbreviation_length} characters"
            )
        if not HeaderParameterInfo.get_valid_height(height)[0]:
            errors.append(f"Height {height} is invalid")
        if not HeaderParameterInfo.is_instrument_valid(
            instrument, self.accepted_values
        ):
            errors.append(
                f"Instrument line {instrument} is invalid. Valid instruments are (case insensitive) "
                f"{sorted(self.accepted_values[Headers.INSTRUMENTS])}."
                """ If multiple instruments are specified, they must be separated by a "," """
            )
        if (
            instrument != "NA"
            and not HeaderParameterInfo.are_instruments_in_listed_instruments(
                instrument, self.listed_instruments
            )
        ):
            errors.append(
                f"Instrument line {instrument} is invalid for the parameter {param}."
                f"All instruments attached to a parameter must be listed in the header instruments."
            )
        return errors
