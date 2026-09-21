from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class KakaoTalkCredentials(BaseModelConfiguration):
    kakaotalk_plus_friend_id: StrictStr = Field(
        default=..., description="KakaoTalk Business Channel ID."
    )
    kakaotalk_sender_key: StrictStr = Field(
        default=..., description="KakaoTalk Sender Key."
    )
