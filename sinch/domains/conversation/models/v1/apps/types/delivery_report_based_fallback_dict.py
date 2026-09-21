from typing import TypedDict
from typing_extensions import NotRequired


class DeliveryReportBasedFallbackDict(TypedDict):
    enabled: NotRequired[bool]
    delivery_report_waiting_time: NotRequired[int]
