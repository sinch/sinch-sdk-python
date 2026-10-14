from typing import Annotated, Union

from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_japan import (
    LineEnterpriseCredentialsJapan,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_thailand import (
    LineEnterpriseCredentialsThailand,
)

LineEnterpriseRegionCredentials = Annotated[
    Union[
        LineEnterpriseCredentialsJapan,
        LineEnterpriseCredentialsThailand,
    ],
    ResolveUnion(),
]
