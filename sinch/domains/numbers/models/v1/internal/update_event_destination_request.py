from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class UpdateEventDestinationRequest(BaseModelConfigurationRequest):
    hmac_secret: Optional[StrictStr] = Field(
        default=None,
        alias="hmacSecret",
        description="The HMAC secret to be updated for the specified project. It must be between 32 and 64 characters, alphanumeric (A-Z, a-z, 0-9) and hyphens (-) only. Regex pattern: ^[a-zA-Z0-9-]{32,64}$",
    )
