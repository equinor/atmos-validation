from __future__ import annotations

from enum import Enum


# pylint: disable=protected-access
class OrderedEnum(str, Enum):
    def __init__(self, _value: str, *args: str, **kwds: str):
        super().__init__(*args, **kwds)
        self.__order = len(self.__class__)

    def __ge__(self, other: ClassificationLevel):  # type: ignore
        if self.__class__ is other.__class__:
            return self.__order >= other.__order
        return NotImplemented

    def __gt__(self, other: ClassificationLevel):  # type: ignore
        if self.__class__ is other.__class__:
            return self.__order > other.__order
        return NotImplemented

    def __le__(self, other: ClassificationLevel):  # type: ignore
        if self.__class__ is other.__class__:
            return self.__order <= other.__order
        return NotImplemented

    def __lt__(self, other: ClassificationLevel):  # type: ignore
        if self.__class__ is other.__class__:
            return self.__order < other.__order
        return NotImplemented


# pylint: enable=protected-access


class ClassificationLevel(OrderedEnum):
    OPEN = "Open"
    INTERNAL = "Internal"
    RESTRICTED = "Restricted"
