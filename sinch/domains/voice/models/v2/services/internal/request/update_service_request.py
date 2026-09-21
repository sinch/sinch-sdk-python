from typing import Optional

from pydantic import Field, StrictBool, StrictStr

from sinch.domains.voice.models.v2.request.idempotency_key_request import (
    IdempotencyKeyRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.service_id_request import (
    ServiceIdRequest,
)
from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    CallBehavior,
)


class UpdateServiceRequest(IdempotencyKeyRequest, ServiceIdRequest):
    name: Optional[StrictStr] = Field(
        default=None,
        description="The name of the service. Must be 1-64 characters, with no leading, trailing, or repeated whitespace. Regex pattern: `^\\S+(\\s+\\S+)*$`.",
    )
    description: Optional[StrictStr] = Field(
        default=None,
        description="A description of the service. Must be at most 255 characters, with no leading, trailing, or repeated whitespace. Regex pattern: `^\\S+(\\s+\\S+)*$`.",
    )
    is_default: Optional[StrictBool] = Field(
        default=None,
        alias="isDefault",
        description="Whether this service is the project default. Setting this to `false` is invalid.",
    )
    call_behavior: Optional[CallBehavior] = Field(
        default=None, alias="callBehavior"
    )
