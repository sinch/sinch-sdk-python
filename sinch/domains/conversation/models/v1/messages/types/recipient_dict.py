from typing import List, TypedDict, Union
from sinch.domains.conversation.models.v1.messages.types.conversation_channel_type import (
    ConversationChannelType,
)


class ChannelRecipientIdentityDict(TypedDict):
    channel: ConversationChannelType
    identity: str


class RecipientIdentifiedByDict(TypedDict):
    channel_identities: List[ChannelRecipientIdentityDict]


class RecipientContactIdDict(TypedDict):
    contact_id: str


RecipientDict = Union[RecipientIdentifiedByDict, RecipientContactIdDict]
