from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.template import (
    TemplateReferenceOmniChannel,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class TemplateReferenceField(BaseModelConfigurationResponse):
    template_reference: Optional[TemplateReferenceOmniChannel] = None
