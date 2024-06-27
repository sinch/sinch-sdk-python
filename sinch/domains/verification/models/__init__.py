from typing import TypedDict, Literal


class VerificationIdentity(TypedDict):
    type: Literal["number"]
    endpoint: str
