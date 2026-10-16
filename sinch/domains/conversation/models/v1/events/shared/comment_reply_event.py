from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class CommentReplyEvent(BaseModelConfiguration):
    text: StrictStr = Field(
        default=..., description="The text of the comment reply."
    )
