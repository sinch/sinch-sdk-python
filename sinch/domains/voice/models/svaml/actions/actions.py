from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, TypedDict
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.voice import Destination, ConferenceDTMFOptions


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


class AnsweringMachineDetection(TypedDict):
    enabled: bool


class CallHeader(TypedDict):
    key: str
    value: str


@dataclass
class HangupAction(SinchRequestBaseModel):
    name: str = "hangup"


@dataclass
class ContinueAction(SinchRequestBaseModel):
    name: str = "continue"


@dataclass
class ConnectPstnAction(SinchRequestBaseModel):
    name: str = "connectPstn"
    number: Optional[str] = None
    locale: Optional[str] = None
    max_duration: Optional[int] = None
    dial_timeout: Optional[int] = None
    cli: Optional[str] = None
    suppress_callbacks: Optional[bool] = None
    dtmf: Optional[str] = None
    indications: Optional[str] = None
    amd: Optional[AnsweringMachineDetection] = None

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("max_duration"):
            payload["maxDuration"] = payload.pop("max_duration")

        if payload.get("dial_timeout"):
            payload["dialTimeout"] = payload.pop("dial_timeout")

        if payload.get("suppress_callbacks"):
            payload["suppressCallbacks"] = payload.pop("suppress_callbacks")

        return payload


@dataclass
class ConnectMxpAction(SinchRequestBaseModel):
    name: str = "connectMxp"
    destination: Optional[Destination] = None
    call_headers: Optional[List[CallHeader]] = None

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("call_headers"):
            payload["callHeaders"] = payload.pop("call_headers")

        return payload


@dataclass
class Option(SinchRequestBaseModel):
    dtmf: str
    action: str


@dataclass
class MenuOption(SinchRequestBaseModel):
    id: str
    main_prompt: Optional[str] = None
    repeat_prompt: Optional[str] = None
    repeats: Optional[int] = None
    max_digits: Optional[int] = None
    timeout_mills: Optional[int] = None
    max_timeout_mills: Optional[int] = None
    options: Optional[List[Option]] = None


@dataclass
class ConnectSipAction(SinchRequestBaseModel):
    destination: Optional[Destination]
    name: str = "connectSip"
    max_duration: Optional[int] = None
    cli: Optional[str] = None
    transport: Optional[str] = None
    suppress_callbacks: Optional[bool] = None
    call_headers: Optional[List[CallHeader]] = None
    moh: Optional[str] = None

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("max_duration"):
            payload["maxDuration"] = payload.pop("max_duration")

        if payload.get("suppress_callbacks"):
            payload["suppressCallbacks"] = payload.pop("suppress_callbacks")

        return payload


@dataclass
class ConnectConfAction(SinchRequestBaseModel):
    destination: Optional[Destination]
    conference_id: str
    name: str = "connectConf"
    conference_dtmf_options: Optional[ConferenceDTMFOptions] = None
    moh: Optional[str] = None


@dataclass
class RunMenuAction(SinchRequestBaseModel):
    name: str = "runMenu"
    barge: Optional[bool] = None
    locale: Optional[str] = None
    main_menu: Optional[str] = None
    enable_voice: Optional[bool] = None
    menus: Optional[List[MenuOption]] = None


@dataclass
class ParkAction(SinchRequestBaseModel):
    name: str = "park"
    locale: Optional[str] = None
    intro_prompt: Optional[str] = None
    hold_prompt: Optional[str] = None
    max_duration: Optional[int] = None
