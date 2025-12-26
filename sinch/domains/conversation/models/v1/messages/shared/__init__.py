from sinch.domains.conversation.models.v1.messages.shared.address_info import (
    AddressInfo,
)
from sinch.domains.conversation.models.v1.messages.shared.agent import Agent
from sinch.domains.conversation.models.v1.messages.shared.app_message_common_props import (
    AppMessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.shared.card_message_internal import (
    CardMessageInternal,
)
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
from sinch.domains.conversation.models.v1.messages.shared.media_properties_internal import (
    MediaPropertiesInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.product_item import (
    ProductItem,
)
from sinch.domains.conversation.models.v1.messages.shared.reason import Reason
from sinch.domains.conversation.models.v1.messages.shared.reason_code import (
    ReasonCode,
)
from sinch.domains.conversation.models.v1.messages.shared.reason_sub_code import (
    ReasonSubCode,
)
from sinch.domains.conversation.models.v1.messages.shared.reply_to_internal import (
    ReplyToInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.template_reference_field import (
    TemplateReferenceField,
)
from sinch.domains.conversation.models.v1.messages.shared.template_reference_internal import (
    TemplateReferenceInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.template_reference_with_version_internal import (
    TemplateReferenceWithVersionInternal,
)

__all__ = [
    "AddressInfo",
    "Agent",
    "AppMessageCommonProps",
    "CardMessageInternal",
    "ChannelIdentity",
    "ChoiceItem",
    "ContactMessageCommonProps",
    "ConversationMessageCommonProps",
    "Coordinates",
    "ListSection",
    "MediaPropertiesInternal",
    "ProductItem",
    "Reason",
    "ReasonCode",
    "ReasonSubCode",
    "ReplyToInternal",
    "TemplateReferenceField",
    "TemplateReferenceInternal",
    "TemplateReferenceWithVersionInternal",
]


def __getattr__(name: str):
    if name == "OmniMessageOverrideInternal":
        from sinch.domains.conversation.models.v1.messages.shared.omni_message_override_internal import (
            OmniMessageOverrideInternal,
        )

        return OmniMessageOverrideInternal
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
