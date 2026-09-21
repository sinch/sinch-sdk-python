from typing import Annotated, Literal, Optional, Union

from pydantic import BeforeValidator, Field, StrictStr

from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)
from sinch.domains.numbers.models.v1.utils.validators import (
    default_voice_configuration_type,
)


class VoiceConfigurationFAX(BaseModelConfigurationRequest):
    type: Literal["FAX"] = "FAX"
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")


class VoiceConfigurationEST(BaseModelConfigurationRequest):
    type: Literal["EST"] = "EST"
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")


class VoiceConfigurationRTC(BaseModelConfigurationRequest):
    type: Literal["RTC"] = "RTC"
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")


class VoiceConfigurationCustom(BaseModelConfigurationRequest):
    type: StrictStr


VoiceConfigurationRequestUnion = Annotated[
    Union[
        VoiceConfigurationRTC,
        VoiceConfigurationEST,
        VoiceConfigurationFAX,
        VoiceConfigurationCustom,
    ],
    BeforeValidator(default_voice_configuration_type),
]
