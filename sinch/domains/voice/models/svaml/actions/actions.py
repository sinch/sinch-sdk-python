from dataclasses import dataclass
from typing import Optional, List, TypedDict
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.voice.models import Destination, ConferenceDTMFOptions


class Action(SinchRequestBaseModel):
    name: str


class AnsweringMachineDetection(TypedDict):
    enabled: bool


class CallHeader(TypedDict):
    key: str
    value: str


@dataclass
class HangupAction(Action):
    name: str = "hangup"


@dataclass
class ContinueAction(Action):
    name: str = "continue"


@dataclass
class ConnectPstnAction(Action):
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
class ConnectMxpAction(Action):
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

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("main_prompt"):
            payload["mainPrompt"] = payload.pop("main_prompt")

        if payload.get("repeat_prompt"):
            payload["repeatPrompt"] = payload.pop("repeat_prompt")

        if payload.get("max_digits"):
            payload["maxDigits"] = payload.pop("max_digits")

        if payload.get("timeout_mills"):
            payload["timeoutMills"] = payload.pop("timeout_mills")

        if payload.get("max_timeout_mills"):
            payload["maxTimeoutMills"] = payload.pop("max_timeout_mills")

        return payload


@dataclass
class ConnectSipAction(Action):
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

        if payload.get("call_headers"):
            payload["callHeaders"] = payload.pop("call_headers")

        return payload


@dataclass
class ConnectConfAction(Action):
    conference_id: str
    name: str = "connectConf"
    conference_dtmf_options: Optional[ConferenceDTMFOptions] = None
    moh: Optional[str] = None

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("conference_id"):
            payload["conferenceId"] = payload.pop("conference_id")

        if payload.get("conference_dtmf_options"):
            payload["conferenceDtmfOptions"] = payload.pop("conference_dtmf_options")

        return payload


@dataclass
class RunMenuAction(Action):
    name: str = "runMenu"
    barge: Optional[bool] = None
    locale: Optional[str] = None
    main_menu: Optional[str] = None
    enable_voice: Optional[bool] = None
    menus: Optional[List[MenuOption]] = None

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("main_menu"):
            payload["mainMenu"] = payload.pop("main_menu")

        if payload.get("enable_voice"):
            payload["enableVoice"] = payload.pop("enable_voice")

        return payload


@dataclass
class ParkAction(Action):
    name: str = "park"
    locale: Optional[str] = None
    intro_prompt: Optional[str] = None
    hold_prompt: Optional[str] = None
    max_duration: Optional[int] = None

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("intro_prompt"):
            payload["introPrompt"] = payload.pop("intro_prompt")

        if payload.get("hold_prompt"):
            payload["holdPrompt"] = payload.pop("hold_prompt")

        if payload.get("max_duration"):
            payload["maxDuration"] = payload.pop("max_duration")

        return payload
