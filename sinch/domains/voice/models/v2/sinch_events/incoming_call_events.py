from typing import List, Optional

from pydantic import Field

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_command import (
    SvamlCommand,
)


class IncomingCallEvents(BaseModelConfiguration):
    on_hangup: Optional[List[SvamlCommand]] = Field(
        default=None,
        alias="onHangup",
        description="SVAML commands to be executed when the call is hung up.",
    )
