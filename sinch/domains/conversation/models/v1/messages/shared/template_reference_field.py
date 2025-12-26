from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.template_reference_with_version_internal import (
    TemplateReferenceWithVersionInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class TemplateReferenceField(BaseModelConfigurationResponse):
    template_reference: Optional[TemplateReferenceWithVersionInternal] = None
