from typing import List, Literal, TypedDict, Union

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.types.call_header_dict import CallHeaderDict
from sinch.domains.voice.models.v2.types.voice_name import VoiceName
from sinch.domains.voice.models.v2.types.voice_name_enum import (
    VoiceNameEnum,
)


class VoiceRelayDetailsDict(TypedDict):
    endpoint: str
    tts_voice: Union[VoiceNameEnum, VoiceName]
    """Name of the default voice to use when synthesizing speech.

    Use ``VoiceNameEnum`` to browse voices with their language, gender and pricing,
    or ``VoiceNameByLanguageEnum`` to browse them grouped by language
    (e.g. ``VoiceNameByLanguageEnum.SPANISH_SPAIN.ABRIL``).
    See https://developers.sinch.com/docs/voice-2.0/api-reference/text-to-speech-voices
    """
    stt_language: str
    enable_interruptions: NotRequired[bool]
    call_headers: NotRequired[List[CallHeaderDict]]


class VoiceRelayDict(TypedDict):
    type: Literal["VOICE_RELAY"]
    voice_relay: VoiceRelayDetailsDict
