from enum import IntEnum


class ConditionType(IntEnum):
    REQUIRED = 1
    FORBIDDEN = -1
