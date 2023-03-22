from enum import Enum


class NumberCapability(Enum):
    SMS = "SMS"
    VOICE = "VOICE"


class NumberType(Enum):
    MOBILE = "MOBILE"
    LOCAL = "LOCAL"
    TOLL_FREE = "TOLL_FREE"
