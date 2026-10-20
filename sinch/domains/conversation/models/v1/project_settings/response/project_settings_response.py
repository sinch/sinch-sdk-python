from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.project_settings.shared.project_settings import (
    ProjectSettings,
)


class ProjectSettingsResponse(BaseModelConfiguration):
    project_id: Optional[StrictStr] = Field(
        default=None, description="The unique ID of the project."
    )
    settings: Optional[ProjectSettings] = Field(
        default=None,
        description="The settings object containing contact settings.",
    )
