from datetime import datetime
from typing import Optional, Literal, Union, Annotated
from pydantic import Field, StrictStr, StrictInt, StrictBool, conlist
from decimal import Decimal
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest, BaseModelConfigResponse

CapabilityType = Annotated[
    conlist(Union[Literal["SMS", "VOICE"], StrictStr], min_length=1),
    Field(default=None)
]

NumberSearchPatternType = Annotated[
    Union[Literal["START", "CONTAINS", "END"], StrictStr],
    Field(default=None)
]

NumberType = Annotated[
    Union[Literal["MOBILE", "LOCAL", "TOLL_FREE"], StrictStr],
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
    trunk_id: Optional[StrictStr] = Field(default=None, alias="truckId")


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
    error_codes: Optional[conlist(StrictStr, min_length=1)] = Field(default=None, alias="errorCodes")


class SmsConfigurationResponse(BaseModelConfigResponse):
    service_plan_id: StrictStr = Field(alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    scheduled_provisioning: Optional[ScheduledProvisioningSmsConfiguration] = (
        Field(default=None, alias="scheduledProvisioning"))


class ScheduledVoiceProvisioningVoiceConfigurationCustom(BaseModelConfigResponse):
    type: StrictStr


class ScheduledVoiceProvisioningVoiceConfigurationFAX(BaseModelConfigResponse):
    type: Literal["FAX"] = "FAX"
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    status: Optional[StatusScheduledProvisioning] = None
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")


class ScheduledVoiceProvisioningVoiceConfigurationEST(BaseModelConfigResponse):
    type: Literal["EST"] = "EST"
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    status: Optional[StatusScheduledProvisioning] = None
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")


class ScheduledVoiceProvisioningVoiceConfigurationRTC(BaseModelConfigResponse):
    type: Literal["RTC"] = "RTC"
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    status: Optional[StatusScheduledProvisioning] = None
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
