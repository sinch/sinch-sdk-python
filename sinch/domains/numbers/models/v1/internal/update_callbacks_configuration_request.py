from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigRequest


class UpdateNumbersCallbacksConfigRequest(BaseModelConfigRequest):
    hmac_secret: Optional[StrictStr] = Field(default=None, alias="hmacSecret")
