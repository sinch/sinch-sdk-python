from typing import Dict, TypedDict

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.template_message_dict import (
    TemplateReferenceChannelSpecificDict,
)


class ChannelTemplateOverrideDict(TypedDict):
    template_reference: NotRequired[TemplateReferenceChannelSpecificDict]
    parameter_mappings: NotRequired[Dict[str, str]]
