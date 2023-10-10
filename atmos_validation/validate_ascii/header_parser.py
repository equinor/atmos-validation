from typing import List, Optional, Set, Tuple

from .header_date import HeaderDate
from .header_metadata import HeaderMetaData
from .header_names import Headers
from .header_parameter_info_list import HeaderParameterInfoList
from .header_position import HeaderPosition
from .utils import get_all_accepted_metadata_values, trim_value


class HeaderParser:
    def __init__(self, lines: List[str]):
        self.lines = lines

    def get_simple_value(
        self,
        key: str,
        errors: List[str],
        accepted_values: Optional[Set[str]] = None,
        split_by: Optional[str] = None,
    ) -> str:
        real_valued = [
            Headers.LOCATION,
            Headers.MOORING,
            Headers.DURATION,
            Headers.NULL_VALUE,
        ]
        for line in self.lines:
            if line.upper().find(key.upper()) > 0:
                try:
                    # Only parse the first colon so as to allow for colons in the text (links for instance)
                    value = trim_value(line.split(":", 1)[1])
                    elements = [value]
                    if split_by:
                        elements = [e.strip() for e in value.split(split_by)]
                    accepted_values_errors = []
                    # print(current_function(), elements, value, line)

                    for element in elements:
                        if accepted_values and element.upper() not in accepted_values:
                            accepted_values_errors.append(
                                f"The value {element} is not acceptable for the metadata item {key}. "
                                f"The value must be in the (case insensitive) set {sorted(list(accepted_values))}"
                            )
                    if accepted_values_errors:
                        errors.extend(accepted_values_errors)
                        return ""
                    return value
                except IndexError:
                    # No colon to separate key from value in metadata line
                    errors.append(f'Missing Colon in line: "{line}"')
        # Could not find the key
        if key in real_valued:
            errors.append(f"Metadata must include a real value for {key}")
        else:
            errors.append(
                f"Metadata must include {key}, if it is unknown, {key}:NA must be specified"
            )
        return ""

    def get_index(self, key: str) -> int:
        index = 0
        for line in self.lines:
            if line.find(key) >= 0:
                return index
            index = index + 1
        return -1

    def get_lines_from(self, index_start: int, index_end: int):
        return self.lines[index_start:index_end]

    def get_header_info(self) -> Tuple[List[str], Optional[HeaderMetaData]]:
        errors = []
        accepted_values = get_all_accepted_metadata_values()
        instruments = self.get_simple_value(
            Headers.INSTRUMENTS,
            errors,
            accepted_values[Headers.INSTRUMENTS],
            split_by=",",
        )
        instrument_spec = self.get_simple_value(Headers.INSTRUMENT_SPEC, errors)
        data_usability_level = self.get_simple_value(
            Headers.DATA_USTABILITY_LEVEL,
            errors,
            accepted_values[Headers.DATA_USTABILITY_LEVEL],
            split_by=",",
        )
        installation_type = self.get_simple_value(
            Headers.INSTALLATION_TYPE,
            errors,
            accepted_values[Headers.INSTALLATION_TYPE],
        )

        parameters = HeaderParameterInfoList(
            self.get_lines_from(
                self.get_index(Headers.PARAMETERS) + 1,
                len(self.lines) - 1,
            ),
            self.lines[-1],
            {e.strip().upper() for e in instruments.split(",")},
            accepted_values,
            instrument_spec,
        )

        position = HeaderPosition(self.get_simple_value(Headers.LOCATION, errors))
        data = HeaderMetaData(
            number_of_header_lines=len(self.lines),
            contractor=self.get_simple_value(Headers.CONTRACTOR, errors),
            final_report=self.get_simple_value(Headers.FINAL_REPORT, errors),
            qc=self.get_simple_value(Headers.QC, errors),
            duration=HeaderDate(self.get_simple_value(Headers.DURATION, errors)),
            mooring_name=self.get_simple_value(Headers.MOORING, errors),
            position=position,
            water_depth=self.get_simple_value(Headers.TOTAL_WATER_DEPTH, errors),
            instruments=instruments,
            data_usability_level=data_usability_level,
            data_history=self.get_simple_value(Headers.DATA_HISTORY, errors),
            project=self.get_simple_value(Headers.PROJECT_NAME, errors),
            averaging_period=self.get_simple_value(Headers.AVERAGING_PERIOD, errors),
            installation_type=installation_type,
            instrument_spec=instrument_spec,
            parameters=parameters,
            empty_value=self.get_simple_value(Headers.NULL_VALUE, errors),
            comments=self.get_simple_value(Headers.COMMENTS, errors),
        )
        if errors:
            return (errors, None)
        return (errors, data)
