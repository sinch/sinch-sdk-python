from dataclasses import dataclass


@dataclass
class Price:
    currency_id: str
    amount: float


@dataclass
class Destination:
    type: str
    endpoint: str
