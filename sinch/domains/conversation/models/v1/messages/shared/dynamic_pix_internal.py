from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.types.pix_key_type import (
    PixKeyType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class DynamicPixInternal(BaseModelConfigurationResponse):
    code: StrictStr = Field(
        ..., description="The dynamic Pix code to be used by the buyer to pay."
    )
    merchant_name: StrictStr = Field(..., description="Account holder name.")
    key: StrictStr = Field(..., description="Pix key.")
    key_type: PixKeyType = Field(..., description="Pix key type.")
