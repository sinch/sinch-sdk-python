from typing import Annotated, Union

from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.credentials.shared.apple_business_chat_credentials import (
    AppleBusinessChatCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.channel_credentials_common_types import (
    ChannelCredentialsCommonTypes,
)
from sinch.domains.conversation.models.v1.credentials.shared.instagram_credentials import (
    InstagramCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_region_credentials import (
    LineEnterpriseRegionCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.kakao_talk_chat_credentials import (
    KakaoTalkChatCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.kakao_talk_credentials import (
    KakaoTalkCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_credentials import (
    LineCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.mms_credentials import (
    MMSCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.static_bearer_credentials import (
    StaticBearerCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.static_token_credentials import (
    StaticTokenCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.telegram_credentials import (
    TelegramCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.we_chat_credentials import (
    WeChatCredentials,
)


class StaticBearerChannelCredentials(ChannelCredentialsCommonTypes):
    static_bearer: StaticBearerCredentials


class StaticTokenChannelCredentials(ChannelCredentialsCommonTypes):
    static_token: StaticTokenCredentials


class MMSChannelCredentials(ChannelCredentialsCommonTypes):
    mms_credentials: MMSCredentials


class KakaoTalkChannelCredentials(ChannelCredentialsCommonTypes):
    kakaotalk_credentials: KakaoTalkCredentials


class TelegramChannelCredentials(ChannelCredentialsCommonTypes):
    telegram_credentials: TelegramCredentials


class LineChannelCredentials(ChannelCredentialsCommonTypes):
    line_credentials: LineCredentials


class LineEnterpriseChannelCredentials(ChannelCredentialsCommonTypes):
    line_enterprise_credentials: LineEnterpriseRegionCredentials


class WeChatChannelCredentials(ChannelCredentialsCommonTypes):
    wechat_credentials: WeChatCredentials


class InstagramChannelCredentials(ChannelCredentialsCommonTypes):
    instagram_credentials: InstagramCredentials


class AppleBusinessChatChannelCredentials(ChannelCredentialsCommonTypes):
    applebc_credentials: AppleBusinessChatCredentials


class KakaoTalkChatChannelCredentials(ChannelCredentialsCommonTypes):
    kakaotalkchat_credentials: KakaoTalkChatCredentials


ConversationChannelCredentials = Annotated[
    Union[
        StaticBearerChannelCredentials,
        StaticTokenChannelCredentials,
        MMSChannelCredentials,
        KakaoTalkChannelCredentials,
        TelegramChannelCredentials,
        LineChannelCredentials,
        LineEnterpriseChannelCredentials,
        WeChatChannelCredentials,
        InstagramChannelCredentials,
        AppleBusinessChatChannelCredentials,
        KakaoTalkChatChannelCredentials,
    ],
    ResolveUnion(
        discriminator="channel",
        tags={
            "WHATSAPP": StaticBearerChannelCredentials,
            "RCS": StaticBearerChannelCredentials,
            "SMS": StaticBearerChannelCredentials,
            "VIBERBM": StaticBearerChannelCredentials,
            "MESSENGER": StaticTokenChannelCredentials,
            "MMS": MMSChannelCredentials,
            "KAKAOTALK": KakaoTalkChannelCredentials,
            "TELEGRAM": TelegramChannelCredentials,
            "LINE": (LineChannelCredentials, LineEnterpriseChannelCredentials),
            "WECHAT": WeChatChannelCredentials,
            "INSTAGRAM": InstagramChannelCredentials,
            "APPLEBC": AppleBusinessChatChannelCredentials,
            "KAKAOTALKCHAT": KakaoTalkChatChannelCredentials,
        },
    ),
]
