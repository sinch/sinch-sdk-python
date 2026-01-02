__all__ = [
    "TemplateMessage",
    "TemplateReferenceChannelSpecific",
    "TemplateReferenceField",
    "TemplateReferenceOmniChannel",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "TemplateMessage":
        from sinch.domains.conversation.models.v1.messages.categories.template.template_message import (
            TemplateMessage,
        )

        return TemplateMessage
    if name == "TemplateReferenceChannelSpecific":
        from sinch.domains.conversation.models.v1.messages.categories.template.template_reference_channel_specific import (
            TemplateReferenceChannelSpecific,
        )

        return TemplateReferenceChannelSpecific
    if name == "TemplateReferenceField":
        from sinch.domains.conversation.models.v1.messages.categories.template.template_reference_field import (
            TemplateReferenceField,
        )

        return TemplateReferenceField
    if name == "TemplateReferenceOmniChannel":
        from sinch.domains.conversation.models.v1.messages.categories.template.template_reference_omni_channel import (
            TemplateReferenceOmniChannel,
        )

        return TemplateReferenceOmniChannel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
