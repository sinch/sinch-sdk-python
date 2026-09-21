from typing import TypedDict

from typing_extensions import NotRequired


class BatchOptionsDict(TypedDict):
    max_cps: NotRequired[int]
    ttl_seconds: NotRequired[int]
