from typing import Literal, Optional, Union

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_error_details import (
    OptErrorDetails,
)
from sinch.domains.conversation.models.v1.types.processing_mode_type import (
    ProcessingModeType,
)


class OptOutNotification(SinchEvent):
    request_id: Optional[StrictStr] = Field(
        default=None,
        description="ID generated when making an opt-out registration request. Can be used to detect duplicates.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact which is the subject of the opt-out. Will be empty if processing_mode is DISPATCH.",
    )
    channel: Optional[ConversationChannelType] = None
    identity: Optional[StrictStr] = Field(
        default=None,
        description="The channel identity. For example, a phone number for SMS, WhatsApp and Viber Business.",
    )
    status: Optional[
        Union[
            Literal[
                "OPT_OUT_SUCCEEDED",
                "OPT_OUT_FAILED",
                "OPT_OUT_STATUS_UNSPECIFIED",
            ],
            StrictStr,
        ]
    ] = Field(default=None, description="Status of the opt-out registration.")
    error_details: Optional[OptErrorDetails] = Field(
        default=None,
        description="This field is populated if the opt-out failed.",
    )
    processing_mode: Optional[ProcessingModeType] = Field(
        default=None,
        description="Whether or not Conversation API should store contacts and conversations for the app. For more information, see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).",
    )
