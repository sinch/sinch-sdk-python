from datetime import date
from typing import List, TypedDict
from typing_extensions import NotRequired


class NameInfoDict(TypedDict):
    full_name: str
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    middle_name: NotRequired[str]
    prefix: NotRequired[str]
    suffix: NotRequired[str]


class PhoneNumberInfoDict(TypedDict):
    phone_number: str
    type: NotRequired[str]


class AddressInfoDict(TypedDict):
    city: NotRequired[str]
    country: NotRequired[str]
    state: NotRequired[str]
    zip: NotRequired[str]
    type: NotRequired[str]
    country_code: NotRequired[str]


class EmailInfoDict(TypedDict):
    email_address: str
    type: NotRequired[str]


class OrganizationInfoDict(TypedDict):
    company: NotRequired[str]
    department: NotRequired[str]
    title: NotRequired[str]


class UrlInfoDict(TypedDict):
    url: str
    type: NotRequired[str]


class ContactInfoMessageDict(TypedDict):
    name: NameInfoDict
    phone_numbers: List[PhoneNumberInfoDict]
    addresses: NotRequired[List[AddressInfoDict]]
    email_addresses: NotRequired[List[EmailInfoDict]]
    organization: NotRequired[OrganizationInfoDict]
    urls: NotRequired[List[UrlInfoDict]]
    birthday: NotRequired[date]
