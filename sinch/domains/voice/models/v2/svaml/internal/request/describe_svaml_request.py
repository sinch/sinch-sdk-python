from pydantic import Field

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_input import SvamlInput


class DescribeSvamlRequest(BaseModelConfiguration):
    svaml: SvamlInput = Field(
        default=..., description="The SVAML payload to describe."
    )
