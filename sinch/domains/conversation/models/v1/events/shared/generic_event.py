from typing import Any, Dict

from pydantic import Field

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class GenericEvent(BaseModelConfiguration):
    payload: Dict[str, Any] = Field(
        default=...,
        description="Arbitrary data set to the event. A valid JSON object.",
    )
