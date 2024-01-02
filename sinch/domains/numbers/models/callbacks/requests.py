from dataclasses import dataclass

from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class UpdateNumbersCallbackConfigurationRequest(SinchRequestBaseModel):
    hmac_secret: str
