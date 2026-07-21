from typing import TypedDict
from typing_extensions import NotRequired


class InstagramCredentialsDict(TypedDict):
    token: str
    business_account_id: NotRequired[str]
