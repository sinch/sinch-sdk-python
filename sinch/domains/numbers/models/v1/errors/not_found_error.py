from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse
from sinch.domains.numbers.models.v1.errors.not_found_error_details import NotFoundErrorDetails
from typing import Optional
from pydantic import ConfigDict, conlist, Field, StrictInt, StrictStr


class NotFoundError(BaseModelConfigurationResponse):
    code: Optional[StrictInt] = Field(default=None, alias="code")
    message: Optional[StrictStr] = Field(default=None, alias="message")
    status: Optional[StrictStr] = Field(default=None, alias="status")
    details: Optional[conlist(NotFoundErrorDetails)] = Field(default=None, alias="details")

    model_config = ConfigDict(populate_by_name=True, alias_generator=BaseModelConfigurationResponse._to_snake_case)
