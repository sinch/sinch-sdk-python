from typing import Union
from sinch.domains.conversation.models.v1.messages.shared.template_reference_field import (
    TemplateReferenceField,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    CardMessageFieldInternal,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    CarouselMessageFieldInternal,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    ChoiceMessageFieldInternal,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    ContactInfoMessageFieldInternal,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    ListMessageFieldInternal,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    LocationMessageFieldInternal,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    MediaMessageFieldInternal,
)
from sinch.domains.conversation.models.v1.messages.fields import (
    TextMessageFieldInternal,
)


OmniMessageOverrideInternal = Union[
    TextMessageFieldInternal,
    MediaMessageFieldInternal,
    TemplateReferenceField,
    ChoiceMessageFieldInternal,
    CardMessageFieldInternal,
    CarouselMessageFieldInternal,
    LocationMessageFieldInternal,
    ContactInfoMessageFieldInternal,
    ListMessageFieldInternal,
]
