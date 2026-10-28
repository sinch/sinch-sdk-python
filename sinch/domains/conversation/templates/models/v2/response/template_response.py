from datetime import datetime
from typing import Optional

from pydantic import Field, StrictInt, StrictStr, conlist

from sinch.domains.conversation.templates.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslation,
)


class TemplateResponse(BaseModelConfiguration):
    id: Optional[StrictStr] = Field(
        default=None,
        description="The id of the template. Specify this yourself during creation. Otherwise, we will generate an ID for you. This must be unique for a given project.",
    )
    description: Optional[StrictStr] = Field(
        default=None, description="The description of the template."
    )
    version: Optional[StrictInt] = Field(
        default=None,
        description="The version of the template. While creating a template, this will be defaulted to 1. When updating a template, you must supply the latest version of the template in order for the update to be successful.",
    )
    default_translation: Optional[StrictStr] = Field(
        default=None,
        description="The default translation to use if not specified. Specified as a BCP-47 `language_code` and the `language_code` must exist in the translations list.",
    )
    translations: Optional[conlist(TemplateTranslation)] = None
    create_time: Optional[datetime] = Field(
        default=None, description="Timestamp of when the template was created."
    )
    update_time: Optional[datetime] = Field(
        default=None, description="Timestamp when the template was updated."
    )
