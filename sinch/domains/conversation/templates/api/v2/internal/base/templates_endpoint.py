from abc import ABC

from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)


class TemplatesEndpoint(ConversationEndpoint, ABC):
    def _get_origin(self, sinch) -> str:
        return sinch.configuration.get_conversation_templates_origin()
