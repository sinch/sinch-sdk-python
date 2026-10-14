from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion

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

VoiceConfiguration = Annotated[
    Union[
        VoiceConfigurationRTC,
        VoiceConfigurationEST,
        VoiceConfigurationFAX,
        VoiceConfigurationCustom,
    ],
    ResolveUnion(
        discriminator="type",
        discriminator_strict=False,
        fallback=VoiceConfigurationCustom,
    ),
]
