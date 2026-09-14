from typing import Literal

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class BridgeCallCommand(BaseModelConfiguration):
    command: Literal["bridgeCall"] = Field(
        default="bridgeCall", description="Command to add the call to a bridge"
    )
    bridge_name: StrictStr = Field(
        default=...,
        alias="bridgeName",
        description="Name of the bridge to join. If no bridge with this name exists in the session, a new one is created automatically.",
    )
