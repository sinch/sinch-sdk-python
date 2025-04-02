from typing import Optional
from pydantic import Field
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest
from sinch.domains.numbers.models.v1.types import NumberTypesRegionsValuesList


class ListAvailableRegionsRequest(BaseModelConfigurationRequest):
    types: Optional[NumberTypesRegionsValuesList] = Field(default=None)
