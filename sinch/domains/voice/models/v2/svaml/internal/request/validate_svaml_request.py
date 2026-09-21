from typing import Optional

from pydantic import Field

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.types.validation_type import (
    ValidationType,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_input import SvamlInput


class ValidateSvamlRequest(BaseModelConfiguration):
    svaml: SvamlInput = Field(
        default=..., description="The SVAML payload to validate."
    )
    validation_type: Optional[ValidationType] = Field(
        default=None,
        alias="validationType",
        description="Controls how strictly the SVAML payload is validated. If omitted, the server applies the default value `NORMAL`.",
    )
