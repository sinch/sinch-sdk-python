from typing import Any, Optional

from pydantic import Field, StrictInt, StrictStr, model_validator

from sinch.domains.conversation.models.v1.credentials.shared.apple_business_chat_credentials import (
    AppleBusinessChatCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.channel_integration_state import (
    ChannelIntegrationState,
)
from sinch.domains.conversation.models.v1.credentials.shared.instagram_credentials import (
    InstagramCredentials,
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
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.internal.mappers.app_mappers import (
    map_channel_credentials_list_to_dict,
)


class _ChannelCredentialsResponseCommon(BaseModelConfiguration):
    callback_secret: Optional[StrictStr] = Field(
        default=None,
        description="The secret used to verify the channel callbacks for channels which support callback verification.The callback verification is not needed for Sinch-managed channels because the callbacks are not leaving Sinch internal networks. Leaving callback_secret empty for channels with callback verification will disable the verification.",
    )
    credential_ordinal_number: Optional[StrictInt] = None
    state: Optional[ChannelIntegrationState] = None
    channel_known_id: Optional[StrictStr] = None


class StaticBearerChannelCredentialsResponse(
    StaticBearerCredentials, _ChannelCredentialsResponseCommon
):
    pass


class StaticTokenChannelCredentialsResponse(
    StaticTokenCredentials, _ChannelCredentialsResponseCommon
):
    pass


class MMSChannelCredentialsResponse(
    MMSCredentials, _ChannelCredentialsResponseCommon
):
    pass


class InstagramChannelCredentialsResponse(
    InstagramCredentials, _ChannelCredentialsResponseCommon
):
    pass


class TelegramChannelCredentialsResponse(
    TelegramCredentials, _ChannelCredentialsResponseCommon
):
    pass


class KakaoTalkChannelCredentialsResponse(
    KakaoTalkCredentials, _ChannelCredentialsResponseCommon
):
    pass


class KakaoTalkChatChannelCredentialsResponse(
    KakaoTalkChatCredentials, _ChannelCredentialsResponseCommon
):
    pass


class LineChannelCredentialsResponse(
    LineCredentials, _ChannelCredentialsResponseCommon
):
    pass


class LineEnterpriseJapanChannelCredentialsResponse(
    LineCredentials, _ChannelCredentialsResponseCommon
):
    pass


class LineEnterpriseThailandChannelCredentialsResponse(
    LineCredentials, _ChannelCredentialsResponseCommon
):
    pass


class WeChatChannelCredentialsResponse(
    WeChatCredentials, _ChannelCredentialsResponseCommon
):
    pass


class AppleBusinessChatChannelCredentialsResponse(
    AppleBusinessChatCredentials, _ChannelCredentialsResponseCommon
):
    pass


class ConversationChannelCredentialsResponse(BaseModelConfiguration):
    whatsapp: Optional[StaticBearerChannelCredentialsResponse] = Field(
        default=None, alias="WHATSAPP"
    )
    rcs: Optional[StaticBearerChannelCredentialsResponse] = Field(
        default=None, alias="RCS"
    )
    sms: Optional[StaticBearerChannelCredentialsResponse] = Field(
        default=None, alias="SMS"
    )
    viberbm: Optional[StaticBearerChannelCredentialsResponse] = Field(
        default=None, alias="VIBERBM"
    )
    messenger: Optional[StaticTokenChannelCredentialsResponse] = Field(
        default=None, alias="MESSENGER"
    )
    mms: Optional[MMSChannelCredentialsResponse] = Field(
        default=None, alias="MMS"
    )
    instagram: Optional[InstagramChannelCredentialsResponse] = Field(
        default=None, alias="INSTAGRAM"
    )
    telegram: Optional[TelegramChannelCredentialsResponse] = Field(
        default=None, alias="TELEGRAM"
    )
    kakaotalk: Optional[KakaoTalkChannelCredentialsResponse] = Field(
        default=None, alias="KAKAOTALK"
    )
    kakaotalkchat: Optional[KakaoTalkChatChannelCredentialsResponse] = Field(
        default=None, alias="KAKAOTALKCHAT"
    )
    line: Optional[LineChannelCredentialsResponse] = Field(
        default=None, alias="LINE"
    )
    line_japan: Optional[LineEnterpriseJapanChannelCredentialsResponse] = (
        Field(default=None, alias="LINE_JAPAN")
    )
    line_thailand: Optional[
        LineEnterpriseThailandChannelCredentialsResponse
    ] = Field(default=None, alias="LINE_THAILAND")
    wechat: Optional[WeChatChannelCredentialsResponse] = Field(
        default=None, alias="WECHAT"
    )
    applebc: Optional[AppleBusinessChatChannelCredentialsResponse] = Field(
        default=None, alias="APPLEBC"
    )

    @model_validator(mode="before")
    @classmethod
    def _map_list_to_channel_map(cls, data: Any) -> Any:
        if isinstance(data, list):
            return map_channel_credentials_list_to_dict(data)
        return data
