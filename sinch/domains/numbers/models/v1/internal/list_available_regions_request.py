from typing import Optional
from pydantic import Field
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigRequest
from sinch.domains.numbers.models.v1.types import NumberTypesRegionsValuesList


class ListAvailableRegionsRequest(BaseModelConfigRequest):
    types: Optional[NumberTypesRegionsValuesList] = Field(default=None)
