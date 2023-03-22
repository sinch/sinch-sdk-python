from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class SMSGroup(SinchBaseModel):
    id: str
    size: int
    created_at: str
    modified_at: str
    name: str
    child_groups: list
    auto_update: dict
