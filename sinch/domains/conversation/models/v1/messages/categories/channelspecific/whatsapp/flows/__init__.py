from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.flow_action_payload import (
    FlowActionPayload,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_body import (
    WhatsAppInteractiveBody,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_footer import (
    WhatsAppInteractiveFooter,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_header_media import (
    WhatsAppInteractiveHeaderMedia,
)


def __getattr__(name: str):
    if name == "FlowChannelSpecificMessage":
        from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.flow_channel_specific_message import (
            FlowChannelSpecificMessage,
        )

        return FlowChannelSpecificMessage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "FlowActionPayload",
    "WhatsAppInteractiveBody",
    "WhatsAppInteractiveFooter",
    "WhatsAppInteractiveHeaderMedia",
    "FlowChannelSpecificMessage",
]
