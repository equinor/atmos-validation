from typing import List, TypedDict


class ResultFileHeader(TypedDict):
    parameter: str
    parameter_key: str
    guid: str
    long: str
    lat: str
    long_used: str
    lat_used: str
    IsMinuteBased: bool
    Minutes: int
    time_from: str
    time_to: str
    year: int


class ResultFile(TypedDict):
    header: ResultFileHeader
    keys: List[int]
    values: List[float]
