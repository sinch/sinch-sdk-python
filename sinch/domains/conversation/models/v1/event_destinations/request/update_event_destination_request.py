from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.event_destinations.internal.event_destination_id_request import (
    EventDestinationIdRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.shared.client_credentials import (
    ClientCredentials,
)
from sinch.domains.conversation.models.v1.event_destinations.types.event_destination_target_type import (
    EventDestinationTargetType,
)
from sinch.domains.conversation.models.v1.event_destinations.types.event_destination_trigger_type import (
    EventDestinationTriggerType,
)


class UpdateEventDestinationRequest(EventDestinationIdRequest):
    app_id: Optional[StrictStr] = Field(
        default=None,
        description="The app that this event destination belongs to.",
    )
    client_credentials: Optional[ClientCredentials] = None
    secret: Optional[StrictStr] = Field(
        default=None,
        description="Optional secret be used to sign contents of events sent by the Conversation API. You can then use the secret to verify the signature.",
    )
    target: Optional[StrictStr] = Field(
        default=None,
        description="The target url where events should be sent to. Maximum URL length is 742. The conversation-api.*.sinch.com subdomains are forbidden.",
    )
    target_type: Optional[EventDestinationTargetType] = None
    triggers: Optional[conlist(EventDestinationTriggerType)] = Field(
        default=None,
        description="An array of triggers that should trigger the event destination and result in an event being sent to the target url. Refer to the list of [Event Destination Triggers](https://developers.sinch.com/docs/conversation/callbacks/#webhook-triggers) for a complete list.",
    )
