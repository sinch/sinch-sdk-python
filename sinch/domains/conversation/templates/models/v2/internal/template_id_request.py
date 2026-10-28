from pydantic import Field, StrictStr

from sinch.domains.conversation.templates.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class TemplateIdRequest(BaseModelConfiguration):
    template_id: StrictStr = Field(
        default=..., description="The ID of the template."
    )
