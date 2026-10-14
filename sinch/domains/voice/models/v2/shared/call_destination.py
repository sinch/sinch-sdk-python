from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion


from sinch.domains.voice.models.v2.shared.phone import Phone
from sinch.domains.voice.models.v2.shared.sip import Sip
from sinch.domains.voice.models.v2.shared.stream import Stream
from sinch.domains.voice.models.v2.shared.voice_relay import VoiceRelay

CallDestination = Annotated[
    Union[
        Phone,
        Sip,
        Stream,
        VoiceRelay,
    ],
    ResolveUnion(discriminator="type"),
]
