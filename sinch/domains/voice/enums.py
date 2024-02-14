from enum import Enum


class CalloutMethod(Enum):
    TTS = "ttsCallout"
    CUSTOM = "customCallout"
    CONFERENCE = "conferenceCallout"
