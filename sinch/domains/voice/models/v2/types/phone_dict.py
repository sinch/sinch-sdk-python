from typing import Literal, TypedDict


class PhoneDetailsDict(TypedDict):
    number: str


class PhoneDict(TypedDict):
    type: Literal["PHONE"]
    phone: PhoneDetailsDict
