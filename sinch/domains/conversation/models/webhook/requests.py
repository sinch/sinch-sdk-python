from dataclasses import dataclass

from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class WebhookRequest(SinchRequestBaseModel):
    app_id: str
    target: str
    triggers: list
    client_credentials: dict
    secret: str
    target_type: str


@dataclass
class CreateConversationWebhookRequest(WebhookRequest):
    pass


@dataclass
class ListConversationWebhookRequest(SinchRequestBaseModel):
    app_id: str


@dataclass
class GetConversationWebhookRequest(SinchRequestBaseModel):
    webhook_id: str


@dataclass
class DeleteConversationWebhookRequest(SinchRequestBaseModel):
    webhook_id: str


@dataclass
class UpdateConversationWebhookRequest(WebhookRequest):
    update_mask: str
    webhook_id: str
