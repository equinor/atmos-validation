from typing import Any, List, Tuple

import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy

from ..schemas import ParameterConfig
from .date_helper import DateHelper
from .header_metadata import HeaderMetaData
from .header_parameter_info import HeaderParameterInfo
from .result_file import ResultFile


class RowParser:
    def __init__(
        self,
        header_info: HeaderMetaData,
        data_rows: List[str],
        base_param_info: List[ParameterConfig],
        remove_duplicates: bool = False,
    ):
        self.header_info = header_info
        self.data_rows = data_rows
        self.remove_duplicates = remove_duplicates
        self.base_param_info = base_param_info

    def validate(self) -> List[str]:
        messages = []
        files_to_add = []
        header_date_values = self.header_info.parameters.filter_items(False)
        header_params = self.header_info.parameters.filter_items(True)
        columns, columns_date_values = self.get_columns(
            header_date_values, header_params
        )
        df = self.get_dataframe(self.data_rows, columns)

        messages = self.validate_columns(df, columns, messages)
        messages = self.validate_rows(df, self.data_rows, messages)
        messages = self.validate_duration_correlation(df, messages)

        if len(messages) > 0:
            return messages

        df.columns = columns
        self.set_dataframe_indexes(df, columns, self.header_info.is_minute_based())
        for parameter in header_params:
            try:
                files_to_add = self.create_rows(
                    df, self.header_info, parameter, columns_date_values, files_to_add
                )
            except Exception as e:
                print(e)
                messages.append("Error in parsing rows for parameter " + parameter.key)
        messages = self.validate_rows_to_save(
            files_to_add, self.data_rows, header_params, messages
        )

        return messages

    # pylint: disable=too-many-arguments
    def create_rows(
        self,
        df: pd.DataFrame,
        header_info: HeaderMetaData,
        parameter: HeaderParameterInfo,
        columns_date_values: List[str],
        files_to_add: List[ResultFile],
    ) -> List[ResultFile]:
        try:
            columns_df = df[columns_date_values + ["period", parameter.key]]
            group_columns_df = columns_df.groupby("YY")
            keys = group_columns_df.groups.keys()
            for year in keys:
                periods, values = self.get_dataframe_values(
                    str(year),
                    parameter.key,
                    group_columns_df,  # type: ignore
                    columns_date_values,
                )
                files_to_add.append(
                    self.create_file(
                        header_info.position.get_latitude(),
                        header_info.position.get_longitude(),
                        parameter,
                        periods,
                        values,
                        header_info.is_minute_based(),
                        int(str(year)),
                    )
                )

        except Exception as e:
            raise e

        return files_to_add

    def validate_duration_correlation(
        self, df: pd.DataFrame, messages: List[str]
    ) -> List[str]:
        yy, mm, dd = (
            self.header_info.parameters.get_index_for_col("YY"),
            self.header_info.parameters.get_index_for_col("MM"),
            self.header_info.parameters.get_index_for_col("DD"),
        )
        try:
            messages.extend(
                self.header_info.duration.validate_correlation(
                    int(df.iat[0, yy]), int(df.iat[0, mm]), int(df.iat[0, dd])
                )
            )
            messages.extend(
                self.header_info.duration.validate_correlation(
                    int(df.iat[df.shape[0] - 1, yy]),
                    int(df.iat[df.shape[0] - 1, mm]),
                    int(df.iat[df.shape[0] - 1, dd]),
                    False,
                )
            )
            return messages
        except Exception as e:
            print("Exception in validate_duration_correlation", e)
            messages.append(
                "Could not verify duration vs dates in rows, unspecified error"
            )
            return messages

    def validate_columns(
        self, df: pd.DataFrame, columns: List[str], messages: List[str]
    ) -> List[str]:
        if len(df.columns) != len(columns):
            messages.append(
                f"Number of columns from header {len(columns)} doesn't match columns in rows {len(df.columns)}"
            )
        return messages

    def validate_rows(
        self, df: pd.DataFrame, data_rows: List[str], messages: List[str]
    ) -> List[str]:
        if len(data_rows) != len(df.index):
            messages.append(
                f"Number of data rows from source {len(data_rows)} "
                f"doesn't match rows targeted to import {len(df.index)}"
            )
        for tup in df.itertuples():
            row_index, row = tup[0], tup[1:]
            for i, cell_content in enumerate(row):
                try:
                    item = self.header_info.parameters.get_item_for_col(i)
                except IndexError:
                    messages.append(
                        f"Less columns than expected at valuerow {row_index}. Column nr {i} does not exist"
                    )
                    continue

                if (
                    cell_content == self.header_info.empty_value
                    and not item.is_time_parameter
                ):
                    continue
                if (
                    cell_content == self.header_info.empty_value
                    and item.is_time_parameter
                ):
                    messages.append(
                        f"Empty value not allowed for time parameter columns row, col: {row_index, item.key}"
                    )
                    continue
                try:
                    float_content = float(cell_content)
                except Exception:
                    messages.append(
                        f"The cell content {cell_content} in row, col {row_index},{item.key} "
                        "is not interpretable as a number (float)"
                    )
                    continue
                if item.is_time_parameter:
                    messages.extend(
                        self.verify_time_param(float_content, item.key, row, item.key)  # type: ignore
                    )
                    continue
                cfg = next(cfg for cfg in self.base_param_info if cfg.key == item.base)
                if cfg.max != "NA" and cfg.max < float_content:
                    messages.append(
                        f"The cell content {cell_content} in row, col {row_index},{item.key} is "
                        f"over maximum range {cfg.max} configured by the base parameter {item.base}"
                    )
                if cfg.min != "NA" and float_content < cfg.min:
                    messages.append(
                        f"The cell content {cell_content} in row, col {row_index},{item.key} is "
                        f"under minimum range {cfg.min} configured by the base parameter {item.base}"
                    )

        return messages

    def verify_time_param(
        self, cell_content: float, time_param: str, row: Tuple[str], col: str
    ) -> List[str]:
        if time_param == "YY" and (cell_content < 1900 or cell_content > 2100):
            return [
                f"The value {cell_content} in row, col {row},{col} is out of range of accepted values"
            ]
        if time_param == "MM" and (cell_content < 1 or cell_content > 31):
            return [
                f"The value {cell_content} in row, col {row},{col} is out of range of accepted values"
            ]
        if time_param == "DD" and (cell_content < 1 or cell_content > 31):
            return [
                f"The value {cell_content} in row, col {row},{col} is out of range of accepted values"
            ]
        if time_param == "HH" and (cell_content < 0 or cell_content > 23):
            return [
                f"The value {cell_content} in row, col {row},{col} is out of range of accepted values"
            ]
        if time_param == "Min" and (cell_content < 0 or cell_content > 59):
            return [
                f"The value {cell_content} in row, col {row},{col} is out of range of accepted values"
            ]
        return []

    def validate_rows_to_save(
        self,
        files_to_save: List[ResultFile],
        data_rows: List[str],
        header_params: List[HeaderParameterInfo],
        messages: List[str],
    ) -> List[str]:
        count = self.number_of_keys_to_save(files_to_save, len(header_params))
        if len(data_rows) != count:
            messages.append(
                f"Duplicates exists, number of rows from source {len(data_rows)} after removal {count}"
            )

        return messages

    def number_of_keys_to_save(
        self, files_to_add: List[ResultFile], number_of_params: int
    ) -> int:
        items = (len(file["values"]) for file in files_to_add)  # type: ignore
        count = 0
        for item in items:
            count = count + int(item)
        return int(count / number_of_params)

    def get_dataframe_values(
        self,
        year: str,
        key: str,
        group_columns_df: DataFrameGroupBy,  # type: ignore
        columns_date_values: List[str],
    ) -> Tuple[Any, Any]:
        group_by_year = group_columns_df.get_group(year)
        if self.remove_duplicates:
            group_by_year = group_by_year.drop_duplicates(
                subset=columns_date_values,
                keep="first",  # type:ignore
            )

        periods = group_by_year["period"].values.tolist()  # type:ignore
        values = group_by_year[key].values  # type:ignore
        return periods, values

    def set_dataframe_indexes(
        self, df: pd.DataFrame, columns: List[str], is_minute_based: bool
    ):
        df.columns = columns
        date_helper = DateHelper()
        if is_minute_based:
            df["period"] = df.apply(lambda row: date_helper.get_minutes(row), axis=1)  # type: ignore
        else:
            df["period"] = df.apply(lambda row: date_helper.get_hours(row), axis=1)  # type: ignore

        df.set_index("period")

    def get_dataframe(self, data_rows: List[str], columns: List[str]) -> pd.DataFrame:
        df = pd.DataFrame(data=[row.split() for row in data_rows], columns=columns)  # type: ignore
        return df

    def get_columns(
        self,
        header_date_values: List[HeaderParameterInfo],
        header_params: List[HeaderParameterInfo],
    ) -> Tuple[List[str], List[str]]:
        columns = []
        columns_date_values = []
        for value in (info.key for info in header_date_values):
            columns_date_values.append(value)
            columns.append(value)
        for value in (info.key for info in header_params):
            columns.append(value)
        return columns, columns_date_values

    def create_file(
        self,
        latitude: str,
        longitude: str,
        parameter: HeaderParameterInfo,
        periods: List[int],
        values: npt.NDArray[np.float32],
        is_minute_based: bool,
        year: int,
    ) -> ResultFile:
        time_from = str(periods[0])
        time_to = str(periods[-1])
        data: ResultFile = {
            "header": {
                "parameter": parameter.name,
                "parameter_key": parameter.key,
                "long": longitude,
                "lat": latitude,
                "long_used": longitude,
                "lat_used": latitude,
                "IsMinuteBased": is_minute_based,
                # Minutes is set later in pipeline if file is minutebased,
                # should probably refactor this to set the Minutes variable in this method,
                # since the logic is the same and all the data required is available here
                "Minutes": 0,
                "guid": "not_set",
                "time_from": time_from,
                "time_to": time_to,
                "year": year,
            },
            "values": values.tolist(),
            "keys": periods,
        }

        return data
