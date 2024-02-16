from enum import Enum


class CalloutMethod(Enum):
    TEXT_TO_SPEECH = "ttsCallout"
    CUSTOM = "customCallout"
    CONFERENCE = "conferenceCallout"
