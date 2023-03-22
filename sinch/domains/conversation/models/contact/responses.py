from dataclasses import dataclass
from typing import List
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.conversation.models import SinchConversationContact


@dataclass
class ListConversationContactsResponse(SinchBaseModel):
    contacts: List[SinchConversationContact]
    next_page_token: str


@dataclass
class CreateConversationContactResponse(SinchConversationContact):
    pass


@dataclass
class DeleteConversationContactResponse(SinchBaseModel):
    pass


@dataclass
class GetConversationContactResponse(SinchConversationContact):
    pass


@dataclass
class MergeConversationContactsResponse(SinchConversationContact):
    pass


@dataclass
class GetConversationChannelProfileResponse(SinchBaseModel):
    profile_name: str


@dataclass
class UpdateConversationContactResponse(SinchConversationContact):
    pass
