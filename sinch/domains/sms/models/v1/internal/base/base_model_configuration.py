import re
from typing import Any
from pydantic import BaseModel, ConfigDict


class BaseModelConfigurationRequest(BaseModel):
    """
    A base model that allows extra fields and converts snake_case to camelCase.
    """

    model_config = ConfigDict(
        # Allows using both alias (camelCase) and field name (snake_case)
        populate_by_name=True,
        # Allows extra values in input
        extra="allow",
    )

    def model_dump_for_query_params(self, exclude_none=True, by_alias=True):
        """
        Serializes the model for use as query parameters.
        Converts list values to comma-separated strings for APIs that expect this format.
        Filters out empty values (empty strings and empty lists).
        """
        data = self.model_dump(exclude_none=exclude_none, by_alias=by_alias)
        filtered_data = {}
        for key, value in data.items():
            if value == "":
                continue
            if isinstance(value, list) and len(value) == 0:
                continue
            if isinstance(value, list):
                filtered_data[key] = ",".join(str(item) for item in value)
            else:
                filtered_data[key] = value
        return filtered_data


class BaseModelConfigurationResponse(BaseModel):
    """
    A base model that allows extra fields and converts camelCase to snake_case
    """

    @staticmethod
    def _to_snake_case(camel_str: str) -> str:
        """Helper to convert camelCase string to snake_case."""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()

    model_config = ConfigDict(
        # Allows using both alias (camelCase) and field name (snake_case)
        populate_by_name=True,
        # Allows extra values in input
        extra="allow",
    )

    def model_post_init(self, __context: Any) -> None:
        """Converts unknown fields from camelCase to snake_case."""
        if self.__pydantic_extra__:
            converted_extra = {
                self._to_snake_case(key): value
                for key, value in self.__pydantic_extra__.items()
            }
            self.__pydantic_extra__.clear()
            self.__pydantic_extra__.update(converted_extra)
