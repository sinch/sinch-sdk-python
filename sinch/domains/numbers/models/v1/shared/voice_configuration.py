from typing import Union

from sinch.domains.numbers.models.v1.shared.voice_configuration_custom import (
    VoiceConfigurationCustom,
)
from sinch.domains.numbers.models.v1.shared.voice_configuration_est import (
    VoiceConfigurationEST,
)
from sinch.domains.numbers.models.v1.shared.voice_configuration_fax import (
    VoiceConfigurationFAX,
)
from sinch.domains.numbers.models.v1.shared.voice_configuration_rtc import (
    VoiceConfigurationRTC,
)

VoiceConfiguration = Union[
    VoiceConfigurationRTC,
    VoiceConfigurationEST,
    VoiceConfigurationFAX,
    VoiceConfigurationCustom,
]
