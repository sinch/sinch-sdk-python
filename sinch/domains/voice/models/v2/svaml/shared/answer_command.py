from typing import Literal

from pydantic import Field

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class AnswerCommand(BaseModelConfiguration):
    command: Literal["answer"] = Field(
        default="answer", description="Answer call"
    )
