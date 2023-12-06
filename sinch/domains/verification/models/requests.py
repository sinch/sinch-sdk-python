from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class StartVerificationRequest(SinchRequestBaseModel):
    identity: dict
    method: str
    reference: str
    custom: str
    flash_call_options: object
