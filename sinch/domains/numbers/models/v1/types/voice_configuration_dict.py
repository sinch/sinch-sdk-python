from typing import Union, Annotated
from pydantic import Field
from sinch.domains.numbers.models.v1.types.voice_configuration_est_dict import (
    VoiceConfigurationESTDict,
)
from sinch.domains.numbers.models.v1.types.voice_configuration_rtc_dict import (
    VoiceConfigurationRTCDict,
)
from sinch.domains.numbers.models.v1.types.voice_configuration_fax_dict import (
    VoiceConfigurationFAXDict,
)
from sinch.domains.numbers.models.v1.types.voice_configuration_custom_dict import (
    VoiceConfigurationCustomDict,
)


VoiceConfigurationDict = Annotated[
    Union[
        VoiceConfigurationFAXDict,
        VoiceConfigurationRTCDict,
        VoiceConfigurationESTDict,
        VoiceConfigurationCustomDict,
    ],
    Field(discriminator="type"),
]
