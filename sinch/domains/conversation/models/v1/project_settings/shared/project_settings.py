from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.project_settings.shared.contact_settings import (
    ContactSettings,
)


class ProjectSettings(BaseModelConfiguration):
    contact_settings: Optional[ContactSettings] = Field(
        default=None,
        description="Settings related to contact management for the project.",
    )
