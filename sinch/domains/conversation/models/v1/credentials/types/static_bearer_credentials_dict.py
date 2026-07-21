from typing import TypedDict


class StaticBearerCredentialsDict(TypedDict):
    claimed_identity: str
    token: str
