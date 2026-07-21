from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class WeChatCredentials(BaseModelConfiguration):
    app_id: StrictStr = Field(
        default=...,
        description="The AppID(Developer ID) for the WeChat channel to which you are connecting.",
    )
    app_secret: StrictStr = Field(
        default=...,
        description="The AppSecret(Developer Password) for the WeChat channel to which you are connecting.",
    )
    token: StrictStr = Field(
        default=...,
        description="The Token for the WeChat channel to which you are connecting.",
    )
    aes_key: StrictStr = Field(
        default=...,
        description="The Encoding AES Key for the WeChat channel to which you are connecting.",
    )
