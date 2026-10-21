from typing import Dict, List

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.send_message_request_body_dict import (
    SendMessageRequestBodyDict,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.templates.models.v2.types.channel_template_override_dict import (
    ChannelTemplateOverrideDict,
)
from sinch.domains.conversation.templates.models.v2.types.template_variable_dict import (
    TemplateVariableDict,
)


class TemplateTranslationDict(SendMessageRequestBodyDict):
    language_code: str
    version: NotRequired[str]
    channel_template_overrides: NotRequired[
        Dict[ConversationChannelType, ChannelTemplateOverrideDict]
    ]
    variables: NotRequired[List[TemplateVariableDict]]
