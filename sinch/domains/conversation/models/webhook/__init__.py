from dataclasses import dataclass

from sinch.core.models.base_model import SinchBaseModel


@dataclass
class ConversationWebhook(SinchBaseModel):
    id: str
    app_id: str
    target: str
    target_type: str
    secret: str
    triggers: list
    client_credentials: dict
