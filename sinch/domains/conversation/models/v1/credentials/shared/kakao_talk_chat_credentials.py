from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class KakaoTalkChatCredentials(BaseModelConfiguration):
    kakaotalk_plus_friend_id: StrictStr = Field(
        default=..., description="Kakaotalk Plus friend ID."
    )
    api_key: Optional[StrictStr] = Field(
        default=None, description="InfoBank API KEY."
    )
