from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class AddressInfo(BaseModelConfigurationResponse):
    city: Optional[StrictStr] = Field(default=None, description="City Name")
    country: Optional[StrictStr] = Field(
        default=None, description="Country Name"
    )
    state: Optional[StrictStr] = Field(
        default=None, description="Name of a state or region of a country."
    )
    zip: Optional[StrictStr] = Field(
        default=None, description="Zip/postal code"
    )
    type: Optional[StrictStr] = Field(
        default=None, description="Address type, e.g. WORK or HOME"
    )
    country_code: Optional[StrictStr] = Field(
        default=None, description="Two letter country code."
    )
