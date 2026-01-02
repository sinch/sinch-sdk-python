from sinch.domains.conversation.models.v1.messages.shared.address_info import (
    AddressInfo,
)
from sinch.domains.conversation.models.v1.messages.shared.agent import Agent
from sinch.domains.conversation.models.v1.messages.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.messages.shared.choice_item import (
    ChoiceItem,
)
from sinch.domains.conversation.models.v1.messages.shared.contact_message_common_props import (
    ContactMessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.shared.conversation_message_common_props import (
    ConversationMessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.shared.coordinates import (
    Coordinates,
)
from sinch.domains.conversation.models.v1.messages.shared.list_section import (
    ListSection,
)
from sinch.domains.conversation.models.v1.messages.shared.product_item import (
    ProductItem,
)
from sinch.domains.conversation.models.v1.messages.shared.reason import Reason
from sinch.domains.conversation.models.v1.messages.shared.reason_sub_code import (
    ReasonSubCode,
)

__all__ = [
    "AddressInfo",
    "Agent",
    "AppMessageCommonProps",
    "ChannelIdentity",
    "ChoiceItem",
    "ContactMessageCommonProps",
    "ConversationMessageCommonProps",
    "Coordinates",
    "ListSection",
    "OmniMessageOverride",
    "ProductItem",
    "Reason",
    "ReasonSubCode",
]


def __getattr__(name: str):
    if name == "OmniMessageOverride":
        from sinch.domains.conversation.models.v1.messages.shared.override.omni_message_override import (
            OmniMessageOverride,
        )

        return OmniMessageOverride
    if name == "AppMessageCommonProps":
        from sinch.domains.conversation.models.v1.messages.shared.app_message_common_props import (
            AppMessageCommonProps,
        )

        return AppMessageCommonProps
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
