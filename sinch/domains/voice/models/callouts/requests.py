from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.voice.models import Destination, ConferenceDTMFOptions


@dataclass
class TextToSpeechVoiceCalloutRequest(SinchRequestBaseModel):
    destination: Destination
    cli: str
    dtmf: str
    domain: str
    custom: str
    locale: str
    text: str
    prompts: str
    enableAce: bool
    enableDice: bool
    enablePie: bool


@dataclass
class ConferenceVoiceCalloutRequest(SinchRequestBaseModel):
    destination: Destination
    conferenceId: str
    cli: str
    conferenceDtmfOptions: ConferenceDTMFOptions
    dtmf: str
    conference: str
    maxDuration: int
    enableAce: bool
    enableDice: bool
    enablePie: bool
    locale: str
    greeting: str
    mohClass: str
    custom: str
    domain: str


@dataclass
class CustomVoiceCalloutRequest(SinchRequestBaseModel):
    cli: str
    destination: Destination
    dtmf: str
    custom: str
    maxDuration: int
    ice: str
    ace: str
    pie: str
