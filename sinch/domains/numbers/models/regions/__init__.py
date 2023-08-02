from dataclasses import dataclass

from sinch.core.models.base_model import SinchBaseModel


@dataclass
class Region(SinchBaseModel):
    region_code: str
    region_name: str
    types: list