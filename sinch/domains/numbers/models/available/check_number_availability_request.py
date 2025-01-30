from pydantic import Field, StrictStr
from sinch.core.models.base_model import BaseModelConfigRequest


class CheckNumberAvailabilityRequest(BaseModelConfigRequest):
    phone_number: StrictStr = Field(alias="phoneNumber")
