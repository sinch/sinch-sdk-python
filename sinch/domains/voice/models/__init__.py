from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Price:
    currency_id: str
    amount: float


@dataclass
class ConferenceParticipant:
    cli: str
    id: str
    duration: int
    muted: bool
    onhold: bool


@dataclass
class ApplicationNumber:
    number: str
    capability: str
    applicationkey: str


class Destination(TypedDict):
    type: str
    endpoint: str


class ConferenceDTMFOptions(TypedDict):
    mode: str
    max_digits: int
    timeout_mills: int
