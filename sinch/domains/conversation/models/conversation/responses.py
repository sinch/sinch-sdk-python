from dataclasses import dataclass
from typing import List
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.conversation.models.conversation import Conversation


@dataclass
class SinchCreateConversationResponse(Conversation):
    pass


@dataclass
class SinchListConversationsResponse(SinchBaseModel):
    conversations: List[Conversation]
    next_page_token: str
    total_size: int


@dataclass
class SinchGetConversationResponse(Conversation):
    pass


@dataclass
class SinchDeleteConversationResponse(SinchBaseModel):
    pass


@dataclass
class SinchUpdateConversationResponse(Conversation):
    pass


@dataclass
class SinchStopConversationResponse(SinchBaseModel):
    pass


@dataclass
class SinchInjectMessageResponse(SinchBaseModel):
    pass
