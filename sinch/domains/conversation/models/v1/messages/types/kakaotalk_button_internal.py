from typing import Union
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_web_link_button_internal import (
    KakaoTalkWebLinkButtonInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_app_link_button_internal import (
    KakaoTalkAppLinkButtonInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_bot_keyword_button_internal import (
    KakaoTalkBotKeywordButtonInternal,
)


KakaoTalkButtonInternalUnion = Union[
    KakaoTalkWebLinkButtonInternal,
    KakaoTalkAppLinkButtonInternal,
    KakaoTalkBotKeywordButtonInternal,
]
