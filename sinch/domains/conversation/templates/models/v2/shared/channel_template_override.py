from typing import Dict, Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.messages.categories.template.template_reference_channel_specific import (
    TemplateReferenceChannelSpecific,
)
from sinch.domains.conversation.templates.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ChannelTemplateOverride(BaseModelConfiguration):
    template_reference: Optional[TemplateReferenceChannelSpecific] = None
    parameter_mappings: Optional[Dict[StrictStr, StrictStr]] = Field(
        default=None,
        description="A mapping between omni-template variables and the channel specific parameters.",
    )
