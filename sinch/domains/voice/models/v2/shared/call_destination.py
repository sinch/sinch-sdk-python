from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from sinch.domains.voice.models.v2.shared.phone import Phone
from sinch.domains.voice.models.v2.shared.sip import Sip
from sinch.domains.voice.models.v2.shared.stream import Stream
from sinch.domains.voice.models.v2.shared.voice_relay import VoiceRelay

CallDestination = Annotated[
    Union[Phone, Sip, Stream, VoiceRelay], Field(discriminator="type")
]
