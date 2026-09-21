from pydantic import StrictStr
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class VoiceConfigurationCustom(BaseModelConfigurationResponse):
    type: StrictStr
