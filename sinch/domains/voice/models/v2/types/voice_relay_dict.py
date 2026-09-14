from typing import List, Literal, TypedDict

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.types.call_header_dict import CallHeaderDict


class VoiceRelayDetailsDict(TypedDict):
    endpoint: str
    tts_voice: str
    stt_language: str
    enable_interruptions: NotRequired[bool]
    call_headers: NotRequired[List[CallHeaderDict]]


class VoiceRelayDict(TypedDict):
    type: Literal["VOICE_RELAY"]
    voice_relay: VoiceRelayDetailsDict
