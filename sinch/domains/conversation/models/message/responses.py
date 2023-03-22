from dataclasses import dataclass
from typing import List
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.conversation.models import SinchConversationMessage


@dataclass
class SendConversationMessageResponse(SinchBaseModel):
    accepted_time: str
    message_id: str


@dataclass
class ListConversationMessagesResponse(SinchBaseModel):
    messages: List[SinchConversationMessage]
    next_page_token: str


@dataclass
class GetConversationMessageResponse(SinchConversationMessage):
    pass


@dataclass
class DeleteConversationMessageResponse(SinchBaseModel):
    pass
