from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.shared.voice_configuration_common import VoiceConfigurationCommon


class VoiceConfigurationFAX(VoiceConfigurationCommon):
    service_id: StrictStr = Field(default=None, alias="serviceId")
