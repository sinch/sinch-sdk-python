from dataclasses import dataclass
from typing import List

from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.conversation.models.templates import ConversationTemplate


@dataclass
class CreateConversationTemplateResponse(ConversationTemplate):
    pass


@dataclass
class ListConversationTemplatesResponse(SinchBaseModel):
    templates: List[ConversationTemplate]


@dataclass
class GetConversationTemplateResponse(ConversationTemplate):
    pass


@dataclass
class DeleteConversationTemplateResponse(SinchBaseModel):
    pass


@dataclass
class UpdateConversationTemplateResponse(ConversationTemplate):
    pass
