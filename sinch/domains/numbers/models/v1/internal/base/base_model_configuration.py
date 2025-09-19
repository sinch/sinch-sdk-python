from typing import Any
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


class BaseModelConfigurationRequest(BaseModel):
    """
    A base model that allows extra fields and converts snake_case to camelCase.
    """

    @classmethod
    def _convert_dict_keys(cls, obj):
        """Recursively convert dictionary keys to camelCase."""
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                # Convert dict key to camelCase
                camel_key = to_camel(key)
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
            return {to_camel(k): self._convert_dict_to_camel_case(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_dict_to_camel_case(i) for i in data]
        return data

    def model_dump(self, **kwargs) -> dict:
        """Converts extra fields from snake_case to camelCase when dumping the model in endpoint."""
        # Get the standard model dump.
        data = super().model_dump(**kwargs)

        # Get extra fields
        extra_data = self.__pydantic_extra__ or {}

        # Merge known + unknown into one dictionary first
        combined = {**data, **extra_data}

        final_dict = {}

        for key, value in combined.items():
            if key in extra_data:
                # This is an unknown field to be converted
                new_key = to_camel(key)
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
                to_snake(key): value for key, value in self.__pydantic_extra__.items()
            }
            self.__pydantic_extra__.clear()
            self.__pydantic_extra__.update(converted_extra)
