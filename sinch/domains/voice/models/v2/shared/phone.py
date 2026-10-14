from typing import Literal

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class PhoneDetails(BaseModelConfiguration):
    number: StrictStr = Field(
        default=...,
        description="""Phone number in E.164 format, between 3 and 16 characters, matching ``^\+[1-9]\d{1,14}$``""",
    )


class Phone(BaseModelConfiguration):
    type: Literal["PHONE"] = Field(
        default="PHONE",
        description="Routes the call to a phone number on the Public Switched Telephone Network (PSTN). The number must be in E.164 format.",
    )
    phone: PhoneDetails = Field(default=...)
