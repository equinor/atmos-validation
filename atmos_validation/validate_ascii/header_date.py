import datetime
from typing import List

from .utils import trim_value


class HeaderDate:
    def __init__(self, date_text: str):
        self.parse_date(date_text)

    def parse_date(self, date: str):
        try:
            dates = date.split("-")
            self.from_date = trim_value(dates[0])
            self.to_date = trim_value(dates[1])
        except Exception as e:
            print(e)

    def get_year(self, dat_str: str) -> int:
        return int(dat_str.split(".")[2])

    def get_month(self, dat_str: str) -> int:
        return int(dat_str.split(".")[1])

    def get_day(self, dat_str: str) -> int:
        return int(dat_str.split(".")[0])

    def get_years(self) -> str:
        from_year = self.get_year(self.from_date)
        to_year = self.get_year(self.to_date)
        years = ""
        while from_year <= to_year:
            years = years + str(from_year) + ","
            from_year = from_year + 1
        return years[0 : (len(years) - 1)]

    def validate_correlation(
        self, yy: int, mm: int, dd: int, correlate_from_date: bool = True
    ) -> List[str]:
        errors = []
        dat_str = self.from_date if correlate_from_date else self.to_date
        year = self.get_year(dat_str)
        month = self.get_month(dat_str)
        day = self.get_day(dat_str)
        if correlate_from_date:
            if year != yy:
                errors.append(
                    "Duration start date does not match the first year in the values"
                )
            if month != mm:
                errors.append(
                    "Duration start date does not match the first month in the values"
                )
            if day != dd:
                errors.append(
                    "Duration start date does not match the first day in the values"
                )
        else:
            if year != yy:
                errors.append(
                    "Duration end date does not match the last year in the values"
                )
            if month != mm:
                errors.append(
                    "Duration end date does not match the last month in the values"
                )
            if day != dd:
                errors.append(
                    "Duration end date does not match the last day in the values"
                )
        return errors

    def validate(self) -> List[str]:
        messages = []
        try:
            messages = messages + self.validate_from_date()
            messages = messages + self.validate_to_date()
        except Exception:
            messages.append("Duration could not be parsed")
        return messages

    def validate_from_date(self) -> List[str]:
        return self.validate_item(self.from_date, "From date")

    def validate_to_date(self) -> List[str]:
        return self.validate_item(self.to_date, "To date")

    def validate_item(self, value: str, text: str) -> List[str]:
        messages = []
        if len(value) == 0:
            messages.append(text + " could not be parsed")
        day, month, year = value.split(".")

        is_valid_date = True
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            is_valid_date = False
        if not is_valid_date:
            messages.append(value + " is not a date")
        return messages
