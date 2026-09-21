from typing import Literal, Optional

from pydantic import Field, StrictBool, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.shared.call_header import CallHeader


class VoiceRelayDetails(BaseModelConfiguration):
    endpoint: StrictStr = Field(
        default=...,
        description="URL to the server that will accept the web-socket request",
    )
    enable_interruptions: Optional[StrictBool] = Field(
        default=None,
        alias="enableInterruptions",
        description='Allow "barge-in" during text-to-speech (TTS) playback.\n\nWhen `true`, TTS playback is interrupted as soon as inbound speech is detected, unless the currently playing content is marked as uninterruptible.\n\nWhen `false`, TTS playback continues uninterrupted, but an interruption signal is still sent over the WebSocket so the client application can choose to stop playback manually if needed.',
    )
    tts_voice: StrictStr = Field(
        default=...,
        alias="ttsVoice",
        description="Name of the voice to be used when synthesizing speech. \n\nThis is the default voice used, if no override voice is provided in the web-socket TTS message.\n\nSupported voices include: Emma, Brian, and others. For a complete list of available voices and their characteristics, see the [Text-to-Speech Voices documentation](/docs/voice/api-reference/text-to-speech-voices).",
    )
    stt_language: StrictStr = Field(
        default=...,
        alias="sttLanguage",
        description="BCP-47 language tag used for speech-to-text transcription of the inbound audio.\n\nThis value determines which language model is used for transcription.",
    )
    call_headers: Optional[conlist(CallHeader)] = Field(
        default=None,
        alias="callHeaders",
        description="Custom headers to be sent in the call setup.",
    )


class VoiceRelay(BaseModelConfiguration):
    type: Literal["VOICE_RELAY"] = Field(
        default="VOICE_RELAY",
        description="Connects to the Voice Relay service to enable STT and TTS services...",
    )
    voice_relay: VoiceRelayDetails = Field(default=..., alias="voiceRelay")
