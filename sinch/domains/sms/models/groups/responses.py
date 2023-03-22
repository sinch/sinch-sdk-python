from dataclasses import dataclass
from typing import List
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.sms.models.groups import SMSGroup


@dataclass
class CreateSMSGroupResponse(SMSGroup):
    pass


@dataclass
class GetSMSGroupResponse(SMSGroup):
    pass


@dataclass
class SinchListSMSGroupResponse(SinchBaseModel):
    page: int
    page_size: int
    count: int
    groups: List[SMSGroup]


@dataclass
class SinchDeleteSMSGroupResponse(SinchBaseModel):
    pass


@dataclass
class SinchGetSMSGroupPhoneNumbersResponse(SinchBaseModel):
    phone_numbers: list


@dataclass
class UpdateSMSGroupResponse(SMSGroup):
    pass


@dataclass
class ReplaceSMSGroupResponse(SMSGroup):
    pass
