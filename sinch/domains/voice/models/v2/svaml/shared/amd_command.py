from typing import Literal, Optional

from pydantic import Field

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.amd_events import AmdEvents


class AmdCommand(BaseModelConfiguration):
    command: Literal["amd"] = Field(
        default="amd",
        description="Command to run Answering Machine Detection on the call",
    )
    events: Optional[AmdEvents] = Field(
        default=None,
        description="SVAML commands to execute based on the answering machine detection result. These events define different call flows depending on whether a human, machine, beep, or unknown entity answers the call.",
    )
