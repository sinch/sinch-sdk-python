import re
from typing import Any
from pydantic import BaseModel, ConfigDict


class BaseModelConfigurationRequest(BaseModel):
    """
    A base model that allows extra fields and converts snake_case to camelCase.
    """

    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Converts snake_case to camelCase while preserving multiple underscores."""
        if not snake_str or "_" not in snake_str:
            return snake_str
        components = snake_str.split('_')
        return components[0].lower() + ''.join(
            (x.capitalize() if x else '_') for x in components[1:]
        )

    @classmethod
    def _convert_dict_keys(cls, obj):
        """Recursively convert dictionary keys to camelCase."""
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                # Convert dict key to camelCase
                camel_key = cls._to_camel_case(key)
                # Recurse on the value
                new_dict[camel_key] = cls._convert_dict_keys(value)
            return new_dict
        elif isinstance(obj, list):
            # Recurse through any list elements (they might be dicts too)
            return [cls._convert_dict_keys(item) for item in obj]
        else:
            return obj

    model_config = ConfigDict(
        # Allows using both alias (camelCase) and field name (snake_case)
        populate_by_name=True,
        # Allows extra values in input
        extra="allow"
    )

    def _convert_dict_to_camel_case(self, data):
        if isinstance(data, dict):
            return {self._to_camel_case(k): self._convert_dict_to_camel_case(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_dict_to_camel_case(i) for i in data]
        return data

    def model_dump(self, **kwargs) -> dict:
        """Converts extra fields from snake_case to camelCase when dumping the model in endpoint."""
        # Get the standard model dump.
        data = super().model_dump(**kwargs)
        if not kwargs or kwargs['by_alias']:
            data = self._convert_dict_to_camel_case(data)

        # Get extra fields
        extra_data = self.__pydantic_extra__ or {}

        # Merge known + unknown into one dictionary first
        combined = {**data, **extra_data}

        final_dict = {}

        for key, value in combined.items():
            if key in extra_data:
                # This is an unknown field to be converted
                new_key = self._to_camel_case(key)
            else:
                # Known field - keep the top-level key as given
                new_key = key

            # Recursively convert any nested dict keys
            converted_value = self._convert_dict_keys(value)

            # Add to final dictionary
            final_dict[new_key] = converted_value

        return final_dict


class BaseModelConfigurationResponse(BaseModel):
    """
    A base model that allows extra fields and converts camelCase to snake_case
    """

    @staticmethod
    def _to_snake_case(camel_str: str) -> str:
        """Helper to convert camelCase string to snake_case."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

    model_config = ConfigDict(
        # Allows using both alias (camelCase) and field name (snake_case)
        populate_by_name=True,
        # Allows extra values in input
        extra="allow",
    )

    def model_post_init(self, __context: Any) -> None:
        """ Converts unknown fields from camelCase to snake_case."""
        if self.__pydantic_extra__:
            converted_extra = {
                self._to_snake_case(key): value for key, value in self.__pydantic_extra__.items()
            }
            self.__pydantic_extra__.clear()
            self.__pydantic_extra__.update(converted_extra)
