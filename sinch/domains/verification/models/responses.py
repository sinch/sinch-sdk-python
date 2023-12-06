from dataclasses import dataclass
from typing import List

from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.numbers.models import Number


@dataclass
class StartVerificationResponse(SinchBaseModel):
    id: str
    method: str
    sms: dict
    _links: list
