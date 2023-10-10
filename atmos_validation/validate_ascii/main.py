import sys
from typing import List, Optional, Tuple

from .header_parser import HeaderMetaData, HeaderParser
from .row_parser import RowParser
from .utils import load_parameter_configs
from .validate_result import ValidateMeasurementResult, ValidateResult

DOCSTRING = """
Usage: python -m atmos_toolkit validate-ascii [SRC_FILENAME]

Validate a standardized .dat, .txt or .LIS file

Args:
    SRC_FILENAME \t \t The source file to validate
"""


def main():
    try:
        src_filename = sys.argv[2]
    except IndexError:
        print(DOCSTRING)
        sys.exit(1)

    try:
        try:
            header_lines, data_rows = read_file_lines(src_filename, "UTF-8")
        except Exception:
            # if for some reason UTF-8 fails, try with ISO-8859-1 encoding
            header_lines, data_rows = read_file_lines(src_filename, "ISO-8859-1")
        if len(header_lines) == 0 or len(data_rows) == 0:
            raise ValueError
    except Exception:
        print(ValidateMeasurementResult(ValidateResult.ERROR, ["Could not read file"]))
        sys.exit(1)

    (messages, header_info) = get_header_meta_data(header_lines)
    if messages:
        print(ValidateMeasurementResult(ValidateResult.ERROR, messages))
        sys.exit(1)

    if not header_info:
        print(
            ValidateMeasurementResult(
                ValidateResult.ERROR,
                ["Unknown validation error, could not get header_info"],
            )
        )
        sys.exit(1)

    messages = header_info.validate()
    messages += validate_with_parameter_configs(header_info)
    if messages:
        print(ValidateMeasurementResult(ValidateResult.ERROR, messages))
        sys.exit(1)

    row_parser = RowParser(
        header_info,
        data_rows,
        load_parameter_configs(),
        remove_duplicates=True,
    )

    messages += row_parser.validate()
    status = ValidateResult.OK
    if len(messages) > 0:
        status = ValidateResult.ERROR
    print(ValidateMeasurementResult(status, messages))


def get_header_meta_data(
    header_lines: List[str],
) -> Tuple[List[str], Optional[HeaderMetaData]]:
    parser = HeaderParser(header_lines)
    return parser.get_header_info()


def read_file_lines(src_filename: str, encoding: str) -> Tuple[List[str], List[str]]:
    header_lines = []
    data_rows = []
    with open(src_filename, "r", encoding=encoding) as file:
        chunk_size = 4096
        line = file.readline(chunk_size)
        while line:
            if line.find("%") == 0:
                header_lines.append(line)
            else:
                if len(line.strip()) > 0:
                    data_rows.append(line.strip())
            line = file.readline(chunk_size)
    return header_lines, data_rows


def validate_with_parameter_configs(header_info: HeaderMetaData) -> List[str]:
    messages = []
    configs = load_parameter_configs()
    for system_parameter in header_info.parameters.filter_items(True):
        key = system_parameter.base
        unit = system_parameter.unit
        cfg = next((cfg for cfg in configs if cfg.key == key), None)
        if not cfg:
            messages.append(f"Base Parameter {key} does not exist")
            messages.append(
                f"Unable to verify unit {unit} for {key}, no such base parameter exist"
            )
            continue
        if not unit == cfg.units:
            messages.append(
                f"The unit {unit} is incorrect for base parameter {key}. The unit should be {cfg.units}"
            )
    return messages
