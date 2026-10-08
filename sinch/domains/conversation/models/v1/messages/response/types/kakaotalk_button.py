from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_web_link_button import (
    KakaoTalkWebLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_app_link_button import (
    KakaoTalkAppLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_bot_keyword_button import (
    KakaoTalkBotKeywordButton,
)


KakaoTalkButton = Annotated[
    Union[
        KakaoTalkWebLinkButton,
        KakaoTalkAppLinkButton,
        KakaoTalkBotKeywordButton,
    ],
    ResolveUnion(discriminator="type", discriminator_strict=False),
]
