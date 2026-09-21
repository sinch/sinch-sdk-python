from typing import Literal, Optional, Union

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class BatchStopResponse(BaseModelConfiguration):
    result: Optional[Union[Literal["STOP_REQUESTED"], StrictStr]] = Field(
        default=None,
        description="State of the batch processing cancellation request.",
    )
