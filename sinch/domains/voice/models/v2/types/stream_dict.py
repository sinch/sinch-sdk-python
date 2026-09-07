from typing import List, Literal, TypedDict, Union

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.types.call_header_dict import CallHeaderDict


class StreamOptionsDict(TypedDict):
    version: NotRequired[int]
    codec: NotRequired[Union[Literal["PCM"], str]]
    sample_rate: NotRequired[
        Union[Literal[8000, 16000, 24000, 44100, 48000, 96000], int]
    ]


class StreamDetailsDict(TypedDict):
    endpoint: str
    stream_options: NotRequired[StreamOptionsDict]
    call_headers: NotRequired[List[CallHeaderDict]]


class StreamDict(TypedDict):
    type: Literal["STREAM"]
    stream: StreamDetailsDict
