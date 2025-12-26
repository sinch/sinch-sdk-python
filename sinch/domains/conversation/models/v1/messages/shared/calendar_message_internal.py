from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CalendarMessageInternal(BaseModelConfigurationResponse):
    title: StrictStr = Field(
        ...,
        description="The title is shown close to the button that leads to open a user calendar.",
    )
    event_start: StrictStr = Field(
        ..., description="The timestamp defines start of a calendar event."
    )
    event_end: StrictStr = Field(
        ..., description="The timestamp defines end of a calendar event."
    )
    event_title: StrictStr = Field(
        ..., description="Title of a calendar event."
    )
    event_description: Optional[StrictStr] = Field(
        default=None, description="Description of a calendar event."
    )
    fallback_url: StrictStr = Field(
        ...,
        description="The URL that is opened when the user cannot open a calendar event directly or channel does not have support for this type.",
    )
