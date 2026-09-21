from typing import Literal, TypedDict


class BridgeCallCommandDict(TypedDict):
    command: Literal["bridgeCall"]
    bridge_name: str
