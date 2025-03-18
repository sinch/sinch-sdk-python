from typing import Optional, Union, Annotated, Literal
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigRequest


class VoiceConfigurationFAX(BaseModelConfigRequest):
    type: Literal["FAX"] = "FAX"
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")


class VoiceConfigurationEST(BaseModelConfigRequest):
    type: Literal["EST"] = "EST"
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")


class VoiceConfigurationRTC(BaseModelConfigRequest):
    type: Literal["RTC"] = "RTC"
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")


class VoiceConfigurationCustom(BaseModelConfigRequest):
    type: StrictStr


VoiceConfigurationType = Annotated[
    Union[VoiceConfigurationFAX, VoiceConfigurationEST, VoiceConfigurationRTC],
    Field(discriminator="type")
]
