from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class RegisterConversationOptInRequest(SinchRequestBaseModel):
    request_id: str
    app_id: str
    channels: list
    recipient: dict
    processing_strategy: str


@dataclass
class RegisterConversationOptOutRequest(SinchRequestBaseModel):
    request_id: str
    app_id: str
    channels: list
    recipient: dict
    processing_strategy: str
