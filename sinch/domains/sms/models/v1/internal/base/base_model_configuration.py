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
