from typing import Literal, TypedDict


class StopRecordingCommandDict(TypedDict):
    command: Literal["stopRecording"]
    recording_name: str
