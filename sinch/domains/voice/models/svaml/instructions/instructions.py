from dataclasses import dataclass
from typing import Optional, List
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class TranscriptionOptions(SinchRequestBaseModel):
    enabled: str = None
    locale: str = None


@dataclass
class RecordingOptions(SinchRequestBaseModel):
    destination_url: str = None
    credentials: str = None
    format: str = None
    notification_events: str = None
    transcription_options: TranscriptionOptions = None

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("destination_url"):
            payload["destinationUrl"] = payload.pop("destination_url")

        if payload.get("notification_events"):
            payload["notificationEvents"] = payload.pop("notification_events")

        if payload.get("transcription_options"):
            payload["transcriptionOptions"] = payload.pop("transcription_options")

        return payload


@dataclass
class PlayFileInstruction(SinchRequestBaseModel):
    ids: List[List[str]]
    locale: str
    name: str = "playFiles"


@dataclass
class SayInstruction(SinchRequestBaseModel):
    name: str = "say"
    text: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class SendDtmfInstruction(SinchRequestBaseModel):
    name: str = "sendDtmf"
    value: Optional[str] = None


@dataclass
class SetCookieInstruction(SinchRequestBaseModel):
    name: str = "setCookie"
    key: Optional[str] = None
    value: Optional[str] = None


@dataclass
class AnswerInstruction(SinchRequestBaseModel):
    name: str = "answer"


@dataclass
class StartRecordingInstruction(SinchRequestBaseModel):
    name: str = "startRecording"
    options: Optional[RecordingOptions] = None


@dataclass
class StopRecordingInstruction(SinchRequestBaseModel):
    name: str = "stopRecording"
