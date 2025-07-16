from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.shared.voice_configuration_common import VoiceConfigurationCommon


class VoiceConfigurationEST(VoiceConfigurationCommon):
    trunk_id: StrictStr = Field(default=None, alias="trunkId")