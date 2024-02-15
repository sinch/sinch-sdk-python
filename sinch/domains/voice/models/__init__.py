from dataclasses import dataclass


@dataclass
class Price:
    currency_id: str
    amount: float
