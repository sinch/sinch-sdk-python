from enum import Enum


class VerificationMethod(Enum):
    SMS = "sms"
    FLASHCALL = "flashCall"
    CALLOUT = "callout"
    SEAMLESS = "seamless"


class VerificationStatus(Enum):
    PENDING = "PENDING"
    SUCCESSFUL = "SUCCESSFUL"
    FAIL = "FAIL"
    DENIED = "DENIED"
    ABORTED = "ABORTED"
    ERROR = "ERROR"
