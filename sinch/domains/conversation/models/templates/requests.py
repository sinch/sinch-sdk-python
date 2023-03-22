from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class CreateConversationTemplateRequest(SinchRequestBaseModel):
    channel: str
    create_time: str
    description: str
    id: str
    translations: list
    default_translation: str
    update_time: str


@dataclass
class GetConversationTemplateRequest(SinchRequestBaseModel):
    template_id: str


@dataclass
class DeleteConversationTemplateRequest(SinchRequestBaseModel):
    template_id: str


@dataclass
class UpdateConversationTemplateRequest(CreateConversationTemplateRequest):
    update_mask: str
    template_id: str
