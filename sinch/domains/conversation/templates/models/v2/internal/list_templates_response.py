from typing import List, Optional

from pydantic import conlist

from sinch.domains.conversation.templates.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.templates.models.v2.response.template_response import (
    TemplateResponse,
)


class ListTemplatesResponse(BaseModelConfiguration):
    templates: Optional[conlist(TemplateResponse)] = None

    @property
    def content(self) -> List[TemplateResponse]:
        return self.templates or []
