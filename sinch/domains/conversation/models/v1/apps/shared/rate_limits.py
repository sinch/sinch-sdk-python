from typing import Optional

from pydantic import Field, StrictInt

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class RateLimits(BaseModelConfiguration):
    inbound: Optional[StrictInt] = Field(
        default=None,
        description="The number of inbound messages/events we process per second, from underlying channels to the app.  The default rate limit is 25.",
    )
    outbound: Optional[StrictInt] = Field(
        default=None,
        description="The number of messages/events we process per second, from the app to the underlying channels. Note that underlying channels may have other rate limits.  The default rate limit is 25.",
    )
    events: Optional[StrictInt] = Field(
        default=None,
        alias="webhooks",
        description="The rate limit of events sent to the event destinations registered for the app. Note that if you have multiple event destinations with shared triggers, multiple events will be sent out for each triggering event. The default rate limit is 25.",
    )
