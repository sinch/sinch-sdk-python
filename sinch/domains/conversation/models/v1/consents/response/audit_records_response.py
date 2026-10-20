from typing import Optional

from pydantic import Field, conlist

from sinch.domains.conversation.models.v1.consents.response.consent_identity_response import (
    ConsentIdentityResponse,
)
from sinch.domains.conversation.models.v1.consents.shared.audit_record import (
    AuditRecord,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class AuditRecordsResponse(BaseModelConfiguration):
    identity: Optional[ConsentIdentityResponse] = None
    audit_records: Optional[conlist(AuditRecord)] = Field(
        default=None,
        description="List of audit records associated with the given identity",
    )
