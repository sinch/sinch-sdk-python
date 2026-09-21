from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.credentials.shared.basic_auth_credentials import (
    BasicAuthCredentials,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class MMSCredentials(BaseModelConfiguration):
    account_id: StrictStr = Field(default=..., description="MMS Account ID.")
    api_key: StrictStr = Field(default=..., description="MMS API Key.")
    basic_auth: Optional[BasicAuthCredentials] = None
