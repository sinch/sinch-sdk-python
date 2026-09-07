from typing import Literal

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class PhoneDetails(BaseModelConfiguration):
    number: StrictStr = Field(default=..., description="E.164 Phone number")


class Phone(BaseModelConfiguration):
    type: Literal["PHONE"] = Field(
        default="PHONE",
        description="Routes the call to a phone number on the Public Switched Telephone Network (PSTN). The number must be in E.164 format.",
    )
    phone: PhoneDetails = Field(default=...)
