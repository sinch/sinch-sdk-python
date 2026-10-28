from typing import Optional

from pydantic import Field, StrictInt, StrictStr, conlist

from sinch.domains.conversation.templates.models.v2.internal.template_id_request import (
    TemplateIdRequest,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslation,
)


class UpdateTemplateRequest(TemplateIdRequest):
    version: StrictInt = Field(
        default=...,
        description="The version of the template. While creating a template, this will be defaulted to 1. When updating a template, you must supply the latest version of the template in order for the update to be successful.",
    )
    description: Optional[StrictStr] = Field(
        default=None, description="The description of the template."
    )
    default_translation: Optional[StrictStr] = Field(
        default=None,
        description="The default translation to use if not specified. Specified as a BCP-47 `language_code` and the `language_code` must exist in the translations list.",
    )
    translations: Optional[conlist(TemplateTranslation)] = None
