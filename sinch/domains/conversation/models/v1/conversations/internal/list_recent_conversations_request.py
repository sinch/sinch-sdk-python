from typing import Literal, Optional, Union

from pydantic import Field, StrictBool, StrictInt, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListRecentConversationsRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(description="The application ID")
    only_active: Optional[StrictBool] = Field(
        default=None,
        description="True if only active conversations should be listed. Default is false.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="The maximum number of conversations to fetch. Defaults to 10 and the maximum value is 50.",
    )
    page_token: Optional[StrictStr] = Field(
        default=None,
        description="Next page token previously returned if any. When specifying this token, make sure to use the same values for the other parameters from the request that originated the token, otherwise the paged results may be inconsistent.",
    )
    order: Optional[Union[Literal["ASC", "DESC"], StrictStr]] = Field(
        default=None,
        description="Whether to sort conversations by newest message first or oldest. Default is DESC (newest first)",
    )
