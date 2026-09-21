from typing import Optional

from pydantic import Field, StrictBool, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ValidateSvamlResponse(BaseModelConfiguration):
    is_valid: StrictBool = Field(
        default=...,
        alias="isValid",
        description="`true` if the submitted SVAML payload passed validation; `false` if one or more errors were found.",
    )
    errors: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="Validation error messages describing why the SVAML payload is invalid.\n\nPresent only when `isValid` is `false`. Each entry identifies a specific problem, including the affected field or command where applicable.",
    )
