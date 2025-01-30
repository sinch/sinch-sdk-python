from datetime import datetime
from typing import List, Optional, Literal
from pydantic import Field, StrictStr, StrictInt, StrictBool, conlist
from decimal import Decimal
from sinch.core.models.base_model import BaseModelConfigResponse


class ScheduledProvisioningSmsConfiguration(BaseModelConfigResponse):
    service_plan_id: Optional[StrictStr] = Field(default=None, alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    status: Optional[StrictStr] = None
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    error_codes: Optional[conlist(StrictStr, min_length=1)] = Field(default=None, alias="errorCodes")


class SmsConfiguration(BaseModelConfigResponse):
    service_plan_id: StrictStr = Field(alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    scheduled_provisioning: Optional[ScheduledProvisioningSmsConfiguration] = (
        Field(default=None, alias="scheduledProvisioning"))


class ScheduledVoiceProvisioningVoiceConfiguration(BaseModelConfigResponse):
    type: Optional[StrictStr] = None
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    status: Optional[StrictStr] = None
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")


class VoiceConfiguration(BaseModelConfigResponse):
    type: StrictStr
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    scheduled_voice_provisioning: Optional[ScheduledVoiceProvisioningVoiceConfiguration] = \
        (Field(default=None, alias="scheduledVoiceProvisioning"))
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")


class Money(BaseModelConfigResponse):
    currency_code: StrictStr = Field(alias="currencyCode")
    amount: Decimal


class Number(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[Literal["MOBILE", "LOCAL", "TOLL_FREE"]] = Field(default=None, alias="type")
    capability: Optional[List[Literal["SMS", "VOICE"]]] = Field(default=None, alias="capability")
    setup_price: Optional[Money] = Field(default=None, alias="setupPrice")
    monthly_price: Optional[Money] = Field(default=None, alias="monthlyPrice")
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    supporting_documentation_required: Optional[StrictBool] = (
        Field(default=None, alias="supportingDocumentationRequired"))
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")
