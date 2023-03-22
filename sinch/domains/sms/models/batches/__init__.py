from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class Batch(SinchRequestBaseModel):
    id: str
    to: list
    from_: str
    body: str
    delivery_report: str
    cancelled: str
    type: str
    campaign_id: str
    created_at: str
    modified_at: str
    send_at: str
    expire_at: str
    callback_url: str = None
    client_reference: str = None
    feedback_enabled: bool = None
    flash_message: bool = None
