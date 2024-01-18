from enum import Enum


class VerificationMethod(Enum):
    SMS = "sms"
    FLASHCALL = "flashCall"
    CALLOUT = "callout"
    SEAMLESS = "seamless"
