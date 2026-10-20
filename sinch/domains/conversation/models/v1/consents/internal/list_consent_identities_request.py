from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from sinch.domains.conversation.models.v1.consents.types.consents_list_type import (
    ConsentsListType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListConsentIdentitiesRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(
        default=...,
        description="The unique ID of the app. You can find this on the [Sinch Dashboard](https://dashboard.sinch.com/convapi/apps).",
    )
    list_type: ConsentsListType = Field(
        default=...,
        description="The consent list type. One of `OPT_OUT_ALL`, `OPT_OUT_MARKETING`, and or `OPT_OUT_NOTIFICATION`.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="Optional. The maximum number of records to fetch. The default is 10 and the maximum is 50.",
    )
    page_token: Optional[StrictStr] = Field(
        default=None,
        description="A page token, received from a previous Get identities from consent list call. Provide this to retrieve a subsequent page.",
    )
