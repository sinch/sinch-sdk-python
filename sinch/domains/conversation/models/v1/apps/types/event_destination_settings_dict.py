from typing import TypedDict

from typing_extensions import NotRequired


class EventDestinationSettingsDict(TypedDict):
    secret_for_overridden_target: NotRequired[str]
