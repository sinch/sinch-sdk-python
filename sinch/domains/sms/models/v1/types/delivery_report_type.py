from typing import Literal, Union
from pydantic import StrictStr


DeliveryReportType = Union[
    Literal["none", "summary", "full", "per_recipient", "per_recipient_final"],
    StrictStr,
]
