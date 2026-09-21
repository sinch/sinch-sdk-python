from typing import Optional
from pydantic import Field, StrictInt, StrictStr
from sinch.domains.conversation.models.v1.credentials.shared.channel_integration_state import (
    ChannelIntegrationState,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class ChannelCredentialsCommonTypes(BaseModelConfiguration):
    callback_secret: Optional[StrictStr] = Field(
        default=None,
        description="The secret used to verify the channel callbacks for channels which support callback verification.The callback verification is not needed for Sinch-managed channels because the callbacks are not leaving Sinch internal networks. Leaving callback_secret empty for channels with callback verification will disable the verification.",
    )
    channel: Optional[ConversationChannelType] = None
    state: Optional[ChannelIntegrationState] = None
    channel_known_id: Optional[StrictStr] = Field(
        default=None,
        description="Additional identifier set by the channel that represents an specific id used by the channel.",
    )
    credential_ordinal_number: Optional[StrictInt] = Field(
        default=None,
        description="The ordinal number of the credential. This field is used when the application supports multiple credential integrations per channel. Currently, this is only applicable to the `LINE` channel. For other channels, this value will always be set to `0`. In the case in which there are multiple credential integrations per channel on a single app, this field must have a unique value for each multi-credential channel entry.",
    )
