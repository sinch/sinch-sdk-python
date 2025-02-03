from pydantic import Field, StrictStr
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest


class CheckNumberAvailabilityRequest(BaseModelConfigRequest):
    phone_number: StrictStr = Field(alias="phoneNumber")
