from typing import Optional

from pydantic import Field, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class CallEvents(BaseModelConfiguration):
    on_answer: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onAnswer",
        description="SVAML commands to be executed when the call is answered",
    )
    on_busy: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onBusy",
        description="SVAML commands to be executed when the call is busy",
    )
    on_reject: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onReject",
        description="SVAML commands to be executed when the call is rejected",
    )
    on_timeout: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onTimeout",
        description="SVAML commands to be executed when the call is timed out",
    )
    on_hangup: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onHangup",
        description="SVAML commands to be executed when the call is hung up",
    )
    on_failure: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onFailure",
        description="SVAML commands to be executed when the call fails",
    )
