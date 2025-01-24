import re
from typing import Any, List, Optional, Dict, Literal
from pydantic import BaseModel, Field


class BaseModelWithExtras(BaseModel):
    """
    A base model that supports extra fields and converts camelCase to snake_case.
    """

    class Config:
        # Allows using both alias (camelCase) and field name (snake_case) in input
        allow_population_by_field_name = True
        # Allow unrecognized fields in input
        extra = "allow"

    def __init__(self, **data):
        # Match input keys against field aliases
        field_alias_map = {
            field.alias if field.alias else name: name
            for name, field in self.__fields__.items()
        }

        # Known fields: Use alias mapping
        known_fields = {
            field_alias_map[key]: self._convert_dict_keys_to_snake_case(value)
            for key, value in data.items()
            if key in field_alias_map
        }

        # Unknown fields: Convert keys to snake_case
        unknown_fields = {
            self._to_snake_case(key): self._convert_dict_keys_to_snake_case(value)
            for key, value in data.items()
            if key not in field_alias_map
        }

        # Initialize the model with known fields
        super().__init__(**known_fields)

        # Add unknown fields as attributes
        for key, value in unknown_fields.items():
            setattr(self, key, value)

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Converts camelCase string to snake_case."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    def _convert_dict_keys_to_snake_case(self, value: Any) -> Any:
        """Recursively converts dictionary keys to snake_case."""
        if isinstance(value, dict):
            return {self._to_snake_case(k): self._convert_dict_keys_to_snake_case(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._convert_dict_keys_to_snake_case(v) for v in value]
        return value


class Number(BaseModelWithExtras):
    phone_number: str = Field(default=None, alias="phoneNumber")
    region_code: str = Field(default=None, alias="regionCode")
    type: Literal["MOBILE", "LOCAL", "TOLL_FREE"] = Field(alias="type")
    capability: List[Literal["SMS", "VOICE"]] = Field(alias="capability")
    setup_price: Optional[dict] = Field(default=None, alias="setupPrice")
    monthly_price: Optional[dict] = Field(default=None, alias="monthlyPrice")
    payment_interval_months: Optional[int] = Field(default=None, alias="paymentIntervalMonths")
    supporting_documentation_required: Optional[bool] = Field(default=None, alias="supportingDocumentationRequired")


class ListAvailableNumbersResponse(BaseModel):
    available_numbers: List[Number] = Field(alias="availableNumbers")

    class Config:
        allow_population_by_field_name = True


class ActivateNumberResponse(BaseModelWithExtras):
    phone_number: str = Field(alias="phoneNumber")
    region_code: str = Field(alias="regionCode")
    type: str
    capability: List[str]
    display_name: Optional[str] = Field(default=None, alias="displayName")
    money: Optional[Dict[str, str]] = None
    payment_interval_months: Optional[int] = Field(default=None, alias="paymentIntervalMonths")
    next_charge_date: Optional[str] = Field(default=None, alias="nextChargeDate")
    expire_at: Optional[str] = Field(default=None, alias="expireAt")
    sms_configuration: Optional[Dict[str, Any]] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[Dict[str, Any]] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[str] = Field(default=None, alias="callbackUrl")


class RentAnyNumberResponse(BaseModelWithExtras):
    phone_number: str = Field(alias="phoneNumber")
    project_id: str = Field(alias="projectId")
    region_code: str = Field(alias="regionCode")
    type: str
    capability: List[str]
    money: Dict[str, str]
    payment_interval_months: int = Field(alias="paymentIntervalMonths")
    next_charge_date: Optional[str] = Field(default=None, alias="nextChargeDate")
    expire_at: Optional[str] = Field(default=None, alias="expireAt")
    sms_configuration: Optional[Dict[str, Any]] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[Dict[str, Any]] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[str] = Field(default=None, alias="callbackUrl")


class CheckNumberAvailabilityResponse(BaseModelWithExtras):
    phone_number: str = Field(alias="phoneNumber")
    region_code: str = Field(alias="regionCode")
    type: Literal["MOBILE", "LOCAL", "TOLL_FREE"] = Field(alias="type")
    capability: List[Literal["SMS", "VOICE"]] = Field(alias="capability")
    setup_price: Dict[str, str] = Field(alias="setupPrice")
    monthly_price: Dict[str, str] = Field(alias="monthlyPrice")
    payment_interval_months: Optional[int] = Field(default=None, alias="paymentIntervalMonths")
    supporting_documentation_required: Optional[bool] = Field(default=None, alias="supportingDocumentationRequired")
