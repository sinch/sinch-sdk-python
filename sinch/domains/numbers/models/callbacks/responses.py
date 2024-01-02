from dataclasses import dataclass

from sinch.core.models.base_model import SinchBaseModel


@dataclass
class NumbersCallbackConfigurationResponse(SinchBaseModel):
    project_id: str
    hmac_secret: str


@dataclass
class GetNumbersCallbackConfigurationResponse(NumbersCallbackConfigurationResponse):
    pass


@dataclass
class UpdateNumbersCallbackConfigurationResponse(NumbersCallbackConfigurationResponse):
    pass
