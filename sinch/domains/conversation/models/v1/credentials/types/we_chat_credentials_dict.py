from typing import TypedDict


class WeChatCredentialsDict(TypedDict):
    app_id: str
    app_secret: str
    token: str
    aes_key: str
