from typing import Optional

from pydantic import StrictStr

from sinch.domains.conversation.templates.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class TemplateVariable(BaseModelConfiguration):
    key: Optional[StrictStr] = None
    preview_value: Optional[StrictStr] = None
