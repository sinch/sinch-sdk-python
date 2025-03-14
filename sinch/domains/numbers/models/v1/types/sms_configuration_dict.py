from typing import TypedDict
from typing_extensions import NotRequired


class SmsConfigurationDict(TypedDict):
    service_plan_id: str
    campaign_id: NotRequired[str]
