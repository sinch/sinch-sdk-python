from dataclasses import dataclass

from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class ListAvailableRegionsForProjectRequest(SinchRequestBaseModel):
    number_type: str
    number_types: list
