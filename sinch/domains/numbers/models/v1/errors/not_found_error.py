from typing import Optional
from pydantic import ConfigDict, conlist, Field, StrictInt, StrictStr
from pydantic.alias_generators import to_snake
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse
from sinch.domains.numbers.models.v1.errors.not_found_error_details import NotFoundErrorDetails


class NotFoundError(BaseModelConfigurationResponse):
    code: Optional[StrictInt] = Field(default=None)
    message: Optional[StrictStr] = Field(default=None)
    status: Optional[StrictStr] = Field(default=None)
    details: Optional[conlist(NotFoundErrorDetails)] = Field(default=None)

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_snake)
