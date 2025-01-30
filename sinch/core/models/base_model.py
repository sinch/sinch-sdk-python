import json
import re
from datetime import datetime
from dataclasses import asdict, dataclass
from typing import Any
from pydantic import BaseModel, ConfigDict


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


class BaseModelConfigRequest(BaseModel):
    """
    A base model that allows extra fields and converts snake_case to camelCase.
    """

    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Converts snake_case to camelCase."""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    model_config = ConfigDict(
        # Allows using both alias (camelCase) and field name (snake_case)
        populate_by_name=True,
        # Allows extra values in input
        extra="allow"
    )

    def model_dump(self, **kwargs) -> dict:
        """Converts extra fields from snake_case to camelCase when dumping the model in endpoint."""
        # Get the standard model dump
        data = super().model_dump(**kwargs)

        # Get extra fields
        extra_data = self.__pydantic_extra__ or {}

        # Convert extra fields to camelCase and collect the original snake_case keys
        converted_extra = {}
        for key, value in extra_data.items():
            camel_case_key = self._to_camel_case(key)
            converted_extra[camel_case_key] = value

        # Remove snake_case keys from `data` before merging converted extras
        for key in extra_data.keys():
            data.pop(key, None)  # Ensure snake_case fields are removed from final output

        # Merge the cleaned base data with the converted extra fields
        return {**data, **converted_extra}


class BaseModelConfigResponse(BaseModel):
    """
    A base model that allows extra fields and converts camelCase to snake_case,
    and serializes datetime fields to ISO format.
    """

    @staticmethod
    def datetime_encoder(v: datetime) -> str:
        """"Converts a datetime object to a string in ISO 8601 format """
        return v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z"

    @staticmethod
    def _to_snake_case(camel_str: str) -> str:
        """Helper to convert camelCase string to snake_case."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

    model_config = ConfigDict(
        # Allows using both alias (camelCase) and field name (snake_case)
        populate_by_name=True,
        # Allows extra values in input
        extra="allow",
        # Custom datetime serialization
        ser_json_typed={datetime: datetime_encoder}
    )

    def model_post_init(self, __context: Any) -> None:
        """ Converts unknown fields from camelCase to snake_case."""
        if self.__pydantic_extra__:
            converted_extra = {
                self._to_snake_case(key): value for key, value in self.__pydantic_extra__.items()
            }
            self.__pydantic_extra__.clear()
            self.__pydantic_extra__.update(converted_extra)
