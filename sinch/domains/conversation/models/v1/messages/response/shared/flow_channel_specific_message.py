from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.whatsapp_common_props import (
    WhatsAppCommonProps,
)
from sinch.domains.conversation.models.v1.messages.response.shared.flow_action_payload import (
    FlowActionPayload,
)


class FlowChannelSpecificMessage(WhatsAppCommonProps):
    flow_id: StrictStr = Field(..., description="ID of the Flow.")
    flow_cta: StrictStr = Field(
        ...,
        description="Text which is displayed on the Call To Action button (20 characters maximum, emoji not supported).",
    )
    flow_token: Optional[StrictStr] = Field(
        default=None, description="Generated token which is an identifier."
    )
    flow_mode: Optional[StrictStr] = Field(
        default="published", description="The mode in which the flow is."
    )
    flow_action: Optional[StrictStr] = Field(
        default="navigate", description="The flow action."
    )
    flow_action_payload: Optional[FlowActionPayload] = None
