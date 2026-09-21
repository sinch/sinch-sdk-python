from typing import TypedDict

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.credentials.types.apple_business_chat_credentials_dict import (
    AppleBusinessChatCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.instagram_credentials_dict import (
    InstagramCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.kakao_talk_chat_credentials_dict import (
    KakaoTalkChatCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.kakao_talk_credentials_dict import (
    KakaoTalkCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.line_credentials_dict import (
    LineCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.line_enterprise_credentials_dict import (
    LineEnterpriseCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.mms_credentials_dict import (
    MMSCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.static_bearer_credentials_dict import (
    StaticBearerCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.static_token_credentials_dict import (
    StaticTokenCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.telegram_credentials_dict import (
    TelegramCredentialsDict,
)
from sinch.domains.conversation.models.v1.credentials.types.we_chat_credentials_dict import (
    WeChatCredentialsDict,
)


class ChannelCredentialsCommonDict(TypedDict):
    callback_secret: NotRequired[str]
    credential_ordinal_number: NotRequired[int]


class StaticBearerChannelCredentialsDict(
    StaticBearerCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class StaticTokenChannelCredentialsDict(
    StaticTokenCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class MMSChannelCredentialsDict(
    MMSCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class InstagramChannelCredentialsDict(
    InstagramCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class TelegramChannelCredentialsDict(
    TelegramCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class KakaoTalkChannelCredentialsDict(
    KakaoTalkCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class KakaoTalkChatChannelCredentialsDict(
    KakaoTalkChatCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class LineChannelCredentialsDict(
    LineCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class LineEnterpriseChannelCredentialsDict(
    LineEnterpriseCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class WeChatChannelCredentialsDict(
    WeChatCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class AppleBusinessChatChannelCredentialsDict(
    AppleBusinessChatCredentialsDict, ChannelCredentialsCommonDict
):
    pass


class ConversationChannelCredentialsDict(TypedDict):
    WHATSAPP: NotRequired[StaticBearerChannelCredentialsDict]
    RCS: NotRequired[StaticBearerChannelCredentialsDict]
    SMS: NotRequired[StaticBearerChannelCredentialsDict]
    VIBERBM: NotRequired[StaticBearerChannelCredentialsDict]
    MESSENGER: NotRequired[StaticTokenChannelCredentialsDict]
    MMS: NotRequired[MMSChannelCredentialsDict]
    INSTAGRAM: NotRequired[InstagramChannelCredentialsDict]
    TELEGRAM: NotRequired[TelegramChannelCredentialsDict]
    KAKAOTALK: NotRequired[KakaoTalkChannelCredentialsDict]
    KAKAOTALKCHAT: NotRequired[KakaoTalkChatChannelCredentialsDict]
    LINE: NotRequired[LineChannelCredentialsDict]
    LINE_JAPAN: NotRequired[LineEnterpriseChannelCredentialsDict]
    LINE_THAILAND: NotRequired[LineEnterpriseChannelCredentialsDict]
    WECHAT: NotRequired[WeChatChannelCredentialsDict]
    APPLEBC: NotRequired[AppleBusinessChatChannelCredentialsDict]
