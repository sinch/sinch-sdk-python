from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class RegisterConversationOptInResponse(SinchBaseModel):
    request_id: str
    opt_in: dict


@dataclass
class RegisterConversationOptOutResponse(SinchBaseModel):
    request_id: str
    opt_out: dict
