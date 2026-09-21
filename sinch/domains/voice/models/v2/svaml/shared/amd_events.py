from typing import Optional

from pydantic import Field, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class AmdEvents(BaseModelConfiguration):
    on_human: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onHuman",
        description="SVAML commands to be executed when a human is detected",
    )
    on_machine: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onMachine",
        description="SVAML commands to be executed when a machine is detected",
    )
    on_beep: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onBeep",
        description="SVAML commands to be executed when a beep is detected",
    )
    on_unknown: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onUnknown",
        description="SVAML commands to be executed when an unknown event is detected",
    )
