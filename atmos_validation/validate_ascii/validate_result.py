from enum import Enum
from typing import List


class ValidateResult(str, Enum):
    OK = "Ok"
    ERROR = "Error"


class ValidateMeasurementResult:
    def __init__(self, status: ValidateResult, messages: List[str]):
        self.status = status
        self.messages = messages

    def __repr__(self) -> str:
        return f"{self.status}, {self.messages}"

    def is_error(self):
        return len(self.messages) > 0
