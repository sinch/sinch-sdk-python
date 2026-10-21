from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.templates.models.v2.internal.template_id_request import (
    TemplateIdRequest,
)


class ListTranslationsRequest(TemplateIdRequest):
    language_code: Optional[StrictStr] = Field(
        default=None, description="The translation's language code."
    )
    translation_version: Optional[StrictStr] = Field(
        default=None, description="The translation's version."
    )
