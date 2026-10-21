from typing import Literal, Optional, Union

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class CommentEvent(SinchEvent):
    id: Optional[StrictStr] = Field(default=None, description="Event's ID")
    text: StrictStr = Field(default=..., description="Comment's text")
    comment_type: Optional[Union[Literal["FEED", "LIVE"], StrictStr]] = Field(
        default=None,
        description="Either LIVE or FEED. Indicates the type of media on which the comment was made.",
    )
    commented_on: Optional[StrictStr] = Field(
        default=None,
        description="Instagram's URL of the live broadcast or the post on which the comment was made (permalink).",
    )
    user: Optional[StrictStr] = Field(
        default=None,
        description="Username of the account that commented in the live broadcast or post.",
    )
