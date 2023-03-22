from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class CreateSMSGroupRequest(SinchRequestBaseModel):
    name: str
    members: list
    child_groups: list
    auto_update: dict


@dataclass
class ListSMSGroupRequest(SinchRequestBaseModel):
    page_size: int
    page: int


@dataclass
class DeleteSMSGroupRequest(SinchRequestBaseModel):
    group_id: str


@dataclass
class GetSMSGroupRequest(SinchRequestBaseModel):
    group_id: str


@dataclass
class GetSMSGroupPhoneNumbersRequest(SinchRequestBaseModel):
    group_id: str


@dataclass
class UpdateSMSGroupRequest(SinchRequestBaseModel):
    group_id: str
    name: str
    add: list
    remove: list
    auto_update: dict
    add_from_group: str
    remove_from_group: str


@dataclass
class ReplaceSMSGroupPhoneNumbersRequest(SinchRequestBaseModel):
    group_id: str
    members: list
    name: str
