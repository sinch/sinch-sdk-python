from datetime import datetime
from typing import Optional, Literal, Union, Annotated, Dict
from pydantic import Field, StrictStr, StrictInt, StrictBool, conlist, ConfigDict, model_validator
from decimal import Decimal
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest, BaseModelConfigResponse

NumberTypeValues = Union[Literal["MOBILE", "LOCAL", "TOLL_FREE"], StrictStr]
CapabilityTypeValues = conlist(Union[Literal["SMS", "VOICE"], StrictStr], min_length=1)
NumberSearchPatternTypeValues = Union[Literal["START", "CONTAINS", "END"], StrictStr]

CapabilityType = Annotated[
    CapabilityTypeValues,
    Field(default=None)
]

NumberSearchPatternType = Annotated[
    NumberSearchPatternTypeValues,
    Field(default=None)
]

NumberType = Annotated[
    NumberTypeValues,
    Field(default=None)
]

StatusScheduledProvisioning = Annotated[
    Union[Literal["WAITING", "IN_PROGRESS", "FAILED"], StrictStr],
    Field(default=None)
]


class SmsConfigurationRequest(BaseModelConfigRequest):
    service_plan_id: StrictStr = Field(alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")


class VoiceConfigurationFAX(BaseModelConfigRequest):
    type: Literal["FAX"] = "FAX"
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")


class VoiceConfigurationEST(BaseModelConfigRequest):
    type: Literal["EST"] = "EST"
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")


class VoiceConfigurationRTC(BaseModelConfigRequest):
    type: Literal["RTC"] = "RTC"
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")


class VoiceConfigurationCustom(BaseModelConfigRequest):
    type: StrictStr


VoiceConfigurationType = Annotated[
    Union[VoiceConfigurationFAX, VoiceConfigurationEST, VoiceConfigurationRTC],
    Field(discriminator="type")
]


class ScheduledProvisioningSmsConfiguration(BaseModelConfigResponse):
    service_plan_id: Optional[StrictStr] = Field(default=None, alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    status: Optional[StatusScheduledProvisioning] = None
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    error_codes: Optional[conlist(StrictStr, min_length=0)] = Field(default=None, alias="errorCodes")


class SmsConfigurationResponse(BaseModelConfigResponse):
    service_plan_id: StrictStr = Field(alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    scheduled_provisioning: Optional[ScheduledProvisioningSmsConfiguration] = (
        Field(default=None, alias="scheduledProvisioning"))


class ScheduledVoiceProvisioningVoiceConfigurationBase(BaseModelConfigResponse):
    type: Literal["FAX", "EST", "RTC"]
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    status: Optional[StatusScheduledProvisioning] = None


class ScheduledVoiceProvisioningVoiceConfigurationCustom(BaseModelConfigResponse):
    type: StrictStr


class ScheduledVoiceProvisioningVoiceConfigurationFAX(ScheduledVoiceProvisioningVoiceConfigurationBase):
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")


class ScheduledVoiceProvisioningVoiceConfigurationEST(ScheduledVoiceProvisioningVoiceConfigurationBase):
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")


class ScheduledVoiceProvisioningVoiceConfigurationRTC(ScheduledVoiceProvisioningVoiceConfigurationBase):
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")


class VoiceConfigurationResponse(BaseModelConfigResponse):
    type: Union[Literal["RTC", "EST", "FAX"], StrictStr]
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    scheduled_voice_provisioning: Union[ScheduledVoiceProvisioningVoiceConfigurationRTC,
                                        ScheduledVoiceProvisioningVoiceConfigurationEST,
                                        ScheduledVoiceProvisioningVoiceConfigurationFAX,
                                        ScheduledVoiceProvisioningVoiceConfigurationCustom,
                                        None] = Field(
        default=None, alias="scheduledVoiceProvisioning"
    )
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")


class Money(BaseModelConfigResponse):
    currency_code: StrictStr = Field(alias="currencyCode")
    amount: Decimal


class Number(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[NumberType] = Field(default=None)
    capability: Optional[CapabilityType] = Field(default=None)
    setup_price: Optional[Money] = Field(default=None, alias="setupPrice")
    monthly_price: Optional[Money] = Field(default=None, alias="monthlyPrice")
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    supporting_documentation_required: Optional[StrictBool] = (
        Field(default=None, alias="supportingDocumentationRequired"))


class NotFoundError(BaseModelConfigResponse):
    code: StrictInt
    message: StrictStr
    status: StrictStr
    details: list[Dict]

    model_config = ConfigDict(populate_by_name=True, alias_generator=BaseModelConfigResponse._to_snake_case)

    @model_validator(mode="before")
    @classmethod
    def transform_details(cls, values: dict) -> dict:
        """Automatically convert details keys to snake_case"""
        if "details" in values and isinstance(values["details"], list):
            values["details"] = [
                {BaseModelConfigResponse._to_snake_case(k): v for k, v in item.items()} for item in values["details"]
            ]
        return values
