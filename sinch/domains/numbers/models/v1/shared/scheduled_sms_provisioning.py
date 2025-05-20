from datetime import datetime
from typing import Optional, Union, Literal
from pydantic import StrictStr, Field, conlist
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse
from sinch.domains.numbers.models.v1.types import StatusScheduledProvisioning


class ScheduledSmsProvisioning(BaseModelConfigurationResponse):
    service_plan_id: Optional[StrictStr] = Field(default=None, alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    status: Optional[StatusScheduledProvisioning] = None
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    error_codes: Optional[
        conlist(
            Union[
                Literal[
                    "CAMPAIGN_EXPIRED",
                    "CAMPAIGN_MNO_REJECTED",
                    "CAMPAIGN_MNO_REVIEW",
                    "CAMPAIGN_MNO_SUSPENDED",
                    "CAMPAIGN_NOT_AVAILABLE",
                    "CAMPAIGN_PENDING_ACCEPTANCE",
                    "CAMPAIGN_PROVISIONING_FAILED",
                    "ERROR_CODE_UNSPECIFIED",
                    "EXCEEDED_10DLC_LIMIT",
                    "INSUFFICIENT_BALANCE",
                    "INTERNAL_ERROR",
                    "INVALID_NNID",
                    "MNO_SHARING_ERROR",
                    "MOCK_CAMPAIGN_NOT_ALLOWED",
                    "NUMBER_PROVISIONING_FAILED",
                    "PARTNER_SERVICE_UNAVAILABLE",
                    "SMS_PROVISIONING_FAILED",
                    "TFN_NOT_ALLOWED",
                ],
                StrictStr,
            ],
            min_length=0,
        )
    ] = Field(default=None, alias="errorCodes")
