from enum import Enum


class CalloutMethod(Enum):
    TEXT_TO_SPEECH = "ttsCallout"
    CUSTOM = "customCallout"
    CONFERENCE = "conferenceCallout"


class VoiceRegion(Enum):
    EUROPE = "euc1"
    NORTH_AMERICA = "use1"
    SOUTH_AMERICA = "sae1"
    SOUTH_EAST_ASIA_1 = "apse1"
    SOUTH_EAST_ASIA_2 = "apse2"
