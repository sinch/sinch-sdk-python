from typing import Optional
from uuid import uuid4

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class IdempotencyKeyRequest(BaseModelConfiguration):
    idempotency_key: Optional[StrictStr] = Field(
        default_factory=lambda: str(uuid4()),
        alias="Idempotency-Key",
        description="Client-generated idempotency key to safely retry requests. Must be between 16 and 128 characters long. If a request with the same key is received within 10 minutes, the cached response from the original request is returned. Using a random UUID (v4) is strongly recommended.",
    )
