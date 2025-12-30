from typing import Optional
from sinch.domains.conversation.models.v1.messages.response.shared.template_reference_with_version import (
    TemplateReferenceWithVersion,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class TemplateReferenceField(BaseModelConfigurationResponse):
    template_reference: Optional[TemplateReferenceWithVersion] = None
