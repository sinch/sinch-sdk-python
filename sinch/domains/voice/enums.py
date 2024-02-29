from enum import Enum


class CalloutMethod(Enum):
    TEXT_TO_SPEECH = "ttsCallout"
    CUSTOM = "customCallout"
    CONFERENCE = "conferenceCallout"


class Region(Enum):
    EUROPE = "euc1"
    NORTH_AMERICA = "use1"
    SOUTH_AMERICA = "sae1"
    SOUTH_EAST_ASIA_1 = "apse1"
    SOUTH_EAST_ASIA_2 = "apse2"


class ConferenceCommand(Enum):
    MUTE = "mute"
    UNMUTE = "unmute"
    ONHOLD = "onhold"
    RESUME = "resume"


class ConferenceMusicOnHold(Enum):
    RING = "ring"
    MUSIC_1 = "music1"
    MUSIC_2 = "music2"
    MUSIC_3 = "music3"
