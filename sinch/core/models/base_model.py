import json
from dataclasses import asdict, dataclass


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
