from typing import Literal, Optional, Union

from pydantic import Field, StrictInt, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.shared.call_header import CallHeader


class StreamOptions(BaseModelConfiguration):
    version: Optional[StrictInt] = Field(
        default=None, description="Defines the version of the stream protocol."
    )
    codec: Optional[Union[Literal["PCM"], StrictStr]] = Field(
        default=None,
        description="Defines the audio codec/format used for the stream audio payload.\n\nCurrently, only `PCM` is supported (uncompressed raw audio). Use `sampleRate` to configure the sampling rate for the stream.",
    )
    sample_rate: Optional[
        Union[Literal[8000, 16000, 24000, 44100, 48000, 96000], StrictInt]
    ] = Field(
        default=None,
        alias="sampleRate",
        description="Defines the audio sampling rate (Hz) used for the stream.\n\nFor calls that traverse the PSTN, audio is typically sampled at 8 kHz, so using a higher value will not improve perceived quality. \n\nHigher sample rates can be useful for non-PSTN scenarios (for example, SIP/streaming paths), but will increase bandwidth usage and processing load.",
    )


class StreamDetails(BaseModelConfiguration):
    endpoint: StrictStr = Field(
        default=...,
        description="WebSocket endpoint that will accept the incoming connection for real-time audio streaming. Must be a valid WebSocket URL using either `ws://` or `wss://` (recommended). The URL must be reachable from the public internet and capable of handling the negotiated stream protocol.",
    )
    stream_options: Optional[StreamOptions] = Field(
        default=None, alias="streamOptions"
    )
    call_headers: Optional[conlist(CallHeader)] = Field(
        default=None,
        alias="callHeaders",
        description="Custom headers to be sent in the call setup.",
    )


class Stream(BaseModelConfiguration):
    type: Literal["STREAM"] = Field(
        default="STREAM",
        description="Routes the call to a WebSocket stream endpoint for real-time audio processing.",
    )
    stream: StreamDetails = Field(default=...)
