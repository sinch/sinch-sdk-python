from typing import Union
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_web_link_button import (
    KakaoTalkWebLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_app_link_button import (
    KakaoTalkAppLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_bot_keyword_button import (
    KakaoTalkBotKeywordButton,
)


KakaoTalkButton = Union[
    KakaoTalkWebLinkButton,
    KakaoTalkAppLinkButton,
    KakaoTalkBotKeywordButton,
]
