from dataclasses import dataclass


@dataclass
class Price:
    currency_id: str
    amount: float


@dataclass
class Destination:
    type: str
    endpoint: str


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
