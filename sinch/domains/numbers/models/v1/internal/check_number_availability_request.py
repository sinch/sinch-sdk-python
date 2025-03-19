from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigRequest


class CheckNumberAvailabilityRequest(BaseModelConfigRequest):
    phone_number: StrictStr = Field(alias="phoneNumber")
