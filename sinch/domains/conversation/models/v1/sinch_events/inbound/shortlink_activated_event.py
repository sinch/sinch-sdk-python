from typing import Optional

from pydantic import Field, StrictBool, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class ShortLinkActivatedEvent(SinchEvent):
    payload: Optional[StrictStr] = Field(
        default=None,
        description="Refers to the payload previously configured to be sent in the postback.",
    )
    title: Optional[StrictStr] = Field(
        default=None, description="Only relevant for the Instagram channel."
    )
    ref: Optional[StrictStr] = Field(
        default=None,
        description="The ref parameter from the shortlink the user visited.",
    )
    source: Optional[StrictStr] = Field(
        default=None,
        description='Defaults to "SHORTLINK" for this type of event.',
    )
    type: Optional[StrictStr] = Field(
        default=None,
        description='The identifier for the referral. For Instagram and Messenger shortlinks, this is always set to "OPEN_THREAD".',
    )
    existing_thread: Optional[StrictBool] = Field(
        default=None,
        description="Set to true if target channel's conversation thread already existed at the moment the shortlink was visited. Set to false if a new conversation thread began when the shortlink was visited.",
    )
