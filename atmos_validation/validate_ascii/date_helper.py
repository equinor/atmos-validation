import datetime
from typing import Any

import pandas as pd


class DateHelper:
    # Seconds from 1900 midnight to 1970 midnight (unix time offset)
    seconds_offset = int(
        (datetime.datetime(1970, 1, 1) - datetime.datetime(1900, 1, 1)).total_seconds()
    )

    def get_hours(self, row: Any) -> int:
        year = row["YY"]
        month = row["MM"]
        day = row["DD"]
        hour = row["HH"]
        base_date = pd.to_datetime("1900-01-01 00:00:00")

        end = datetime.datetime(int(year), int(month), int(day), int(hour), 0)
        diff = end - base_date
        return int(diff.total_seconds() / 3600)

    def get_minutes(self, row: Any) -> int:
        year = row["YY"]
        month = row["MM"]
        day = row["DD"]
        hour = row["HH"]
        minutes = row["Min"]
        base_date = pd.to_datetime("1900-01-01 00:00:00")

        end = datetime.datetime(
            int(year), int(month), int(day), int(hour), int(minutes)
        )
        diff = end - base_date
        seconds = diff.total_seconds()
        minutes = seconds / 60
        return int(minutes)
