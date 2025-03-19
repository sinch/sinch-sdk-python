from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.errors.error_details import ErrorDetails
from typing import Optional
from pydantic import ConfigDict, conlist, Field, StrictInt, StrictStr


class NotFoundError(BaseModelConfigResponse):
    code: Optional[StrictInt] = Field(default=None, alias="code")
    message: Optional[StrictStr] = Field(default=None, alias="message")
    status: Optional[StrictStr] = Field(default=None, alias="status")
    details: Optional[conlist(ErrorDetails, min_length=1)] = Field(default=None, alias="details")

    model_config = ConfigDict(populate_by_name=True, alias_generator=BaseModelConfigResponse._to_snake_case)
