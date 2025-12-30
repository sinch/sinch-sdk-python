from typing import Dict, Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.shared.template_reference import (
    TemplateReference,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class TemplateMessage(BaseModelConfigurationResponse):
    channel_template: Optional[Dict[str, TemplateReference]] = Field(
        default=None,
        description="Optional. Channel specific template reference with parameters per channel. The channel template if exists overrides the omnichannel template. At least one of `channel_template` or `omni_template` needs to be present. The key in the map must point to a valid conversation channel as defined by the enum ConversationChannel.",
    )
    omni_template: Optional[TemplateReference] = None
