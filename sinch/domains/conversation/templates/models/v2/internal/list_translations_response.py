from typing import List, Optional

from pydantic import conlist

from sinch.domains.conversation.templates.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslation,
)


class ListTranslationsResponse(BaseModelConfiguration):
    translations: Optional[conlist(TemplateTranslation)] = None

    @property
    def content(self) -> List[TemplateTranslation]:
        return self.translations or []
