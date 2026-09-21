from typing import TypedDict
from typing_extensions import NotRequired


class KakaoTalkChatCredentialsDict(TypedDict):
    kakaotalk_plus_friend_id: str
    api_key: NotRequired[str]
