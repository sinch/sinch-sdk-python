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


class MusicOnHold(Enum):
    RING = "ring"
    MUSIC_1 = "music1"
    MUSIC_2 = "music2"
    MUSIC_3 = "music3"


class ConferenceDTMFOptionsMode(Enum):
    IGNORE = "ignore"
    FORWARD = "forward"
    DETECT = "detect"


class Indications(Enum):
    AUSTRIA = "at"
    AUSTRALIA = "au"
    BULGARIA = "bg"
    BRAZIL = "br"
    BELGIUM = "be"
    SWITZERLAND = "ch"
    CHILE = "cl"
    CHINA = "cn"
    CZECH_REPUBLIC = "cz"
    GERMANY = "de"
    DENMARK = "dk"
    ESTONIA = "ee"
    SPAIN = "es"
    FINLAND = "fi"
    FRANCE = "fr"
    GREECE = "gr"
    HUNGARY = "hu"
    ISRAEL = "il"
    INDIA = "in"
    ITALY = "it"
    LITHUANIA = "lt"
    JAPAN = "jp"
    MEXICO = "mx"
    MALAYSIA = "my"
    NETHERLANDS = "nl"
    NORWAY = "no"
    NEW_ZEALAND = "nz"
    PHILIPPINES = "ph"
    POLAND = "pl"
    PORTUGAL = "pt"
    RUSSIA = "ru"
    SWEDEN = "se"
    SINGAPORE = "sg"
    THAILAND = "th"
    UNITED_KINGDOM = "uk"
    UNITED_STATES = "us"
    TAIWAN = "tw"
    VENEZUELA = "ve"
    SOUTH_AFRICA = "za"
