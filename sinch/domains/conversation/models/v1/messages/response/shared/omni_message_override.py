from typing import Union
from sinch.domains.conversation.models.v1.messages.shared.template_reference_field import (
    TemplateReferenceField,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    CardMessageField,
    CarouselMessageField,
    ChoiceMessageField,
    ContactInfoMessageField,
    ListMessageField,
    LocationMessageField,
    MediaMessageField,
    TextMessageField,
)


OmniMessageOverride = Union[
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
