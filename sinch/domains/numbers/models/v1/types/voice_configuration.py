from typing import Union
from sinch.domains.numbers.models.v1.shared import (
    VoiceConfigurationEST, VoiceConfigurationRTC, VoiceConfigurationFAX
)

VoiceConfiguration = Union[VoiceConfigurationEST, VoiceConfigurationRTC, VoiceConfigurationFAX]
