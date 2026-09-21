from typing import Optional

from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials_response import (
    ConversationChannelCredentialsResponse,
)


class AppCustomResponse(AppResponse):
    channel_credentials: Optional[ConversationChannelCredentialsResponse] = (
        None
    )
