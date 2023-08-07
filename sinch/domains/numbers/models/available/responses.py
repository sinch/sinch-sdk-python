from dataclasses import dataclass
from typing import List

from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.numbers.models import Number


@dataclass
class ListAvailableNumbersResponse(SinchBaseModel):
    available_numbers: List[Number]


@dataclass
class ActivateNumberResponse(SinchBaseModel):
    phone_number: str
    region_code: str
    type: str
    capability: list


@dataclass
class RentAnyNumberResponse(SinchBaseModel):
    phone_number: str
    project_id: str
    region_code: str
    type: str
    capability: list
    money: dict
    payment_interval_months: int
    next_charge_date: str
    expire_at: str
    sms_configuration: object
    voice_configuration: object
    callback_url: str


@dataclass
class CheckNumberAvailabilityResponse(Number):
    pass
