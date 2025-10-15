from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class NumberRequest(BaseModelConfigurationRequest):
    phone_number: StrictStr = Field(alias="phoneNumber")
