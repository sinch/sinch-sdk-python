from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal, Optional, Union
from pydantic import ConfigDict, conlist, Field, StrictBool, StrictInt, StrictStr
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest, BaseModelConfigResponse


NumberTypeValues = Union[Literal["MOBILE", "LOCAL", "TOLL_FREE"], StrictStr]
CapabilityTypeValuesList = conlist(Union[Literal["SMS", "VOICE"], StrictStr], min_length=1)
NumberSearchPatternTypeValues = Union[Literal["START", "CONTAINS", "END"], StrictStr]
OrderByValues = Union[Literal["PHONE_NUMBER", "DISPLAY_NAME"], StrictStr]

CapabilityType = Annotated[
    CapabilityTypeValuesList,
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


class ActiveNumber(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    project_id: Optional[StrictStr] = Field(default=None, alias="projectId")
    display_name: Optional[StrictStr] = Field(default=None, alias="displayName")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[NumberType] = Field(default=None)
    capabilities: Optional[CapabilityType] = Field(default=None)
    money: Optional[Money] = Field(default=None)
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    next_charge_date: Optional[datetime] = Field(default=None, alias="nextChargeDate")
    expire_at: Optional[datetime] = Field(default=None, alias="expireAt")
    sms_configuration: Optional[SmsConfigurationResponse] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[VoiceConfigurationResponse] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")


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


class ErrorDetails(BaseModelConfigResponse):
    type: Optional[StrictStr] = Field(default=None, alias="type")
    resource_type: Optional[StrictStr] = Field(default=None, alias="resourceType")
    resource_name: Optional[StrictStr] = Field(default=None, alias="resourceName")
    owner: Optional[StrictStr] = Field(default=None, alias="owner")
    description: Optional[StrictStr] = Field(default=None, alias="description")


class NotFoundError(BaseModelConfigResponse):
    code: Optional[StrictInt] = Field(default=None, alias="code")
    message: Optional[StrictStr] = Field(default=None, alias="message")
    status: Optional[StrictStr] = Field(default=None, alias="status")
    details: Optional[list[ErrorDetails]] = Field(default=None, alias="details")

    model_config = ConfigDict(populate_by_name=True, alias_generator=BaseModelConfigResponse._to_snake_case)
