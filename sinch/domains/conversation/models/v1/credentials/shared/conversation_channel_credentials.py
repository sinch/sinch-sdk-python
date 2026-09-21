from typing import Annotated, Union
from pydantic import Discriminator, Tag
from sinch.domains.conversation.models.v1.credentials.shared.apple_business_chat_credentials import (
    AppleBusinessChatCredentials,
)
from sinch.domains.conversation.models.v1.internal.mappers.channel_credentials_mappers import (
    discriminate_channel_credentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.channel_credentials_common_types import (
    ChannelCredentialsCommonTypes,
)
from sinch.domains.conversation.models.v1.credentials.shared.instagram_credentials import (
    InstagramCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_japan import (
    LineEnterpriseCredentialsJapan,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_thailand import (
    LineEnterpriseCredentialsThailand,
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
    line_enterprise_credentials: Union[
        LineEnterpriseCredentialsJapan, LineEnterpriseCredentialsThailand
    ]


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
        Annotated[StaticBearerChannelCredentials, Tag("WHATSAPP")],
        Annotated[StaticBearerChannelCredentials, Tag("RCS")],
        Annotated[StaticBearerChannelCredentials, Tag("SMS")],
        Annotated[StaticBearerChannelCredentials, Tag("VIBERBM")],
        Annotated[StaticTokenChannelCredentials, Tag("MESSENGER")],
        Annotated[MMSChannelCredentials, Tag("MMS")],
        Annotated[KakaoTalkChannelCredentials, Tag("KAKAOTALK")],
        Annotated[TelegramChannelCredentials, Tag("TELEGRAM")],
        Annotated[
            Union[LineChannelCredentials, LineEnterpriseChannelCredentials],
            Tag("LINE"),
        ],
        Annotated[WeChatChannelCredentials, Tag("WECHAT")],
        Annotated[InstagramChannelCredentials, Tag("INSTAGRAM")],
        Annotated[AppleBusinessChatChannelCredentials, Tag("APPLEBC")],
        Annotated[KakaoTalkChatChannelCredentials, Tag("KAKAOTALKCHAT")],
    ],
    Discriminator(discriminate_channel_credentials),
]
