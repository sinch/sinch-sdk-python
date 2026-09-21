from typing import Optional
from pydantic import Field, StrictBool
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials import (
    LineEnterpriseCredentials,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class LineEnterpriseCredentialsJapan(BaseModelConfiguration):
    line_japan: LineEnterpriseCredentials
    is_default: Optional[StrictBool] = Field(
        default=None,
        description="When an app contains multiple LINE or LINE Enterprise credentials, one of the credentials needs to be defined as the default. Setting this property to `true` marks the corresponding credentials as the default credentials.",
    )
