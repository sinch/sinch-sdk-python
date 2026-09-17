from typing_extensions import NotRequired, TypedDict


class EventDestinationConfigurationDict(TypedDict):
    url: str
    fallback_url: NotRequired[str]
