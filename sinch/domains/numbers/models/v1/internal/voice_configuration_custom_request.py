from pydantic import StrictStr
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest


class VoiceConfigurationCustom(BaseModelConfigurationRequest):
    type: StrictStr
