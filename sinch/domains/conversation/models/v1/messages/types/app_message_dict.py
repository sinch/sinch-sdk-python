from typing import Any, Dict

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.events.types.agent_dict import (
    AgentDict,
)
from sinch.domains.conversation.models.v1.messages.types.send_message_request_body_dict import (
    SendMessageRequestBodyDict,
)


class AppMessageDict(SendMessageRequestBodyDict):
    explicit_channel_message: NotRequired[Dict[str, str]]
    explicit_channel_omni_message: NotRequired[Dict[str, Dict[str, Any]]]
    channel_specific_message: NotRequired[Dict[str, Dict[str, Any]]]
    agent: NotRequired[AgentDict]
