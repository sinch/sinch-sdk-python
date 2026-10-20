from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListAuditRecordsRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(
        default=...,
        description="The unique ID of the app. You can find this on the [Sinch Dashboard](https://dashboard.sinch.com/convapi/apps).",
    )
    identity: StrictStr = Field(
        default=...,
        description="An identity to use on Consent audit records queries.",
    )
