from typing import Union


def _get_omni_message_override_union():
    """Lazy import to avoid circular dependencies."""
    from sinch.domains.conversation.models.v1.messages.categories.card.card_message_field import (
        CardMessageField,
    )
    from sinch.domains.conversation.models.v1.messages.categories.carousel.carousel_message_field import (
        CarouselMessageField,
    )
    from sinch.domains.conversation.models.v1.messages.categories.choice.choice_message_field import (
        ChoiceMessageField,
    )
    from sinch.domains.conversation.models.v1.messages.categories.contactinfo.contact_info_message_field import (
        ContactInfoMessageField,
    )
    from sinch.domains.conversation.models.v1.messages.categories.list.list_message_field import (
        ListMessageField,
    )
    from sinch.domains.conversation.models.v1.messages.categories.location.location_message_field import (
        LocationMessageField,
    )
    from sinch.domains.conversation.models.v1.messages.categories.media.media_message_field import (
        MediaMessageField,
    )
    from sinch.domains.conversation.models.v1.messages.categories.template.template_reference_field import (
        TemplateReferenceField,
    )
    from sinch.domains.conversation.models.v1.messages.categories.text.text_message_field import (
        TextMessageField,
    )

    return Union[
        TextMessageField,
        MediaMessageField,
        TemplateReferenceField,
        ChoiceMessageField,
        CardMessageField,
        CarouselMessageField,
        LocationMessageField,
        ContactInfoMessageField,
        ListMessageField,
    ]


def __getattr__(name: str):
    if name == "OmniMessageOverride":
        return _get_omni_message_override_union()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
