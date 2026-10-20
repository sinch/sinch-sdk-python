from datetime import datetime as DateTime
from typing import Literal, Union

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.consents.types.consents_list_type import (
    ConsentsListType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class AuditRecordResponse(BaseModelConfiguration):
    origin: Union[Literal["ORIGIN_API", "ORIGIN_MO"], StrictStr] = Field(
        default=...,
        description="The origin from the opt-out or opt-in. This could be the Batch API or an MO (when matched with an end-user MO).",
    )
    operation: Union[
        Literal["OPERATION_INSERT", "OPERATION_UPDATE", "OPERATION_DELETE"],
        StrictStr,
    ] = Field(
        default=...,
        description="The operation that the audit record refers to. Can be INSERT, UPDATE or DELETE.",
    )
    list_type: ConsentsListType = Field(
        default=...,
        description="The list type of the consent list the audit record refers to.",
    )
    project_id: StrictStr = Field(
        default=...,
        description="The project ID associated with the consent list the audit record refers to.",
    )
    app_id: StrictStr = Field(
        default=...,
        description="The app ID associated with the consent list the audit record refers to.",
    )
    datetime: DateTime = Field(
        default=...,
        description="Datetime of when the consent list audit record happened.",
    )
