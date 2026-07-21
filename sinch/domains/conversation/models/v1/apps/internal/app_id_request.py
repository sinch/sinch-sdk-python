from pydantic import StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class AppIdRequest(BaseModelConfiguration):
    app_id: StrictStr
