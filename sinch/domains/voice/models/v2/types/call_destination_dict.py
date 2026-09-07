from typing import Union

from sinch.domains.voice.models.v2.types.phone_dict import PhoneDict
from sinch.domains.voice.models.v2.types.sip_dict import SipDict
from sinch.domains.voice.models.v2.types.stream_dict import StreamDict
from sinch.domains.voice.models.v2.types.voice_relay_dict import (
    VoiceRelayDict,
)

CallDestinationDict = Union[PhoneDict, SipDict, StreamDict, VoiceRelayDict]
