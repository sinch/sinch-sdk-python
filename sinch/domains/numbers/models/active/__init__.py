from dataclasses import dataclass

from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.numbers.enums import NumberType, NumberCapability
from sinch.domains.numbers.models.active.list_active_numbers_request import ListActiveNumbersRequest
from sinch.domains.numbers.models.active.list_active_numbers_response import ListActiveNumbersResponse

__all__ = [
    "ListActiveNumbersRequest",
    "ListActiveNumbersResponse"
]


@dataclass
class ActiveNumber(SinchBaseModel):
    phone_number: str
    project_id: str
    display_name: str
    region_code: str
    type: NumberType
    capability: NumberCapability
    money: dict
    payment_interval_months: int
    next_charge_date: str
    expire_at: str
    sms_configuration: dict
    voice_configuration: dict
