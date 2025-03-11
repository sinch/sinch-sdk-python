from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal import BaseModelConfigRequest


class CheckNumberAvailabilityRequest(BaseModelConfigRequest):
    phone_number: StrictStr = Field(alias="phoneNumber")
