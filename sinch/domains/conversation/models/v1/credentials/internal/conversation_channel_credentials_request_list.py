from typing import Annotated

from pydantic import BeforeValidator, conlist

from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import (
    ConversationChannelCredentials,
)
from sinch.domains.conversation.models.v1.internal.mappers.app_mappers import (
    map_channel_credentials_dict_to_list,
)

ConversationChannelCredentialsRequestList = Annotated[
    conlist(ConversationChannelCredentials),
    BeforeValidator(map_channel_credentials_dict_to_list),
]
