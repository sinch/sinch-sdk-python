import json
from dataclasses import asdict, dataclass
from pydantic import BaseModel


@dataclass
class SinchBaseModel:
    def as_dict(self):
        return asdict(self)

    def as_json(self):
        return json.dumps(self.as_dict())


@dataclass
class SinchRequestBaseModel(SinchBaseModel):
    def as_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


class BaseModelConfig(BaseModel):
    class Config:
        # Allows using both alias (camelCase) and field name (snake_case) in input
        allow_population_by_field_name = True
        # Allows extra values in input
        extra = "allow"
