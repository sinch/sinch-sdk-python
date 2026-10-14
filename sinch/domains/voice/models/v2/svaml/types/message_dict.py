from typing import Literal, TypedDict, Union

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.types.voice_name import VoiceName
from sinch.domains.voice.models.v2.types.voice_name_enum import (
    VoiceNameEnum,
)


class SayDict(TypedDict):
    text: str
    voice_name: Union[VoiceNameEnum, VoiceName]
    """Name of the voice to use for text-to-speech synthesis.

    Use ``VoiceNameEnum`` to browse voices with their language, gender and pricing,
    or ``VoiceNameByLanguageEnum`` to browse them grouped by language
    (e.g. ``VoiceNameByLanguageEnum.SPANISH_SPAIN.ABRIL``).
    See https://developers.sinch.com/docs/voice-2.0/api-reference/text-to-speech-voices
    """
    format: NotRequired[Union[Literal["TEXT", "SSML"], str]]


class SayMessageDict(TypedDict):
    type: Literal["SAY"]
    say: SayDict


class PlayDict(TypedDict):
    url: str


class PlayMessageDict(TypedDict):
    type: Literal["PLAY"]
    play: PlayDict


MessageDict = Union[SayMessageDict, PlayMessageDict]
