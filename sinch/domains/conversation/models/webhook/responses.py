from dataclasses import dataclass
from typing import List

from sinch.domains.conversation.models.webhook import ConversationWebhook
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class CreateWebhookResponse(ConversationWebhook):
    pass


@dataclass
class UpdateWebhookResponse(ConversationWebhook):
    pass


@dataclass
class SinchListWebhooksResponse(SinchBaseModel):
    webhooks: List[ConversationWebhook]


@dataclass
class GetWebhookResponse(ConversationWebhook):
    pass


@dataclass
class SinchDeleteWebhookResponse(SinchBaseModel):
    pass
