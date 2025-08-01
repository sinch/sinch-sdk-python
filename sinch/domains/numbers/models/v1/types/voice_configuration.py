from typing import Union
from sinch.domains.numbers.models.v1.shared.voice_configuration_est import VoiceConfigurationEST
from sinch.domains.numbers.models.v1.shared.voice_configuration_rtc import VoiceConfigurationRTC
from sinch.domains.numbers.models.v1.shared.voice_configuration_fax import VoiceConfigurationFAX

VoiceConfiguration = Union[VoiceConfigurationEST, VoiceConfigurationRTC, VoiceConfigurationFAX]
