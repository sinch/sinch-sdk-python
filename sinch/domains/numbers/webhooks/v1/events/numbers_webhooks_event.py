from datetime import datetime
from typing import Optional, Union, Literal
from pydantic import Field, StrictStr
from sinch.domains.numbers.webhooks.v1.internal import WebhookEvent


class NumbersWebhooksEvent(WebhookEvent):
    event_id: Optional[StrictStr] = Field(default=None, alias="eventId")
    timestamp: Optional[datetime] = Field(default=None)
    project_id: Optional[StrictStr] = Field(default=None, alias="projectId")
    resource_id: Optional[StrictStr] = Field(default=None, alias="resourceId")
    resource_type: Optional[Union[Literal["ACTIVE_NUMBER"], StrictStr]] = Field(default=None, alias="resourceType")
    event_type: Optional[Union[Literal[
        "PROVISIONING_TO_CAMPAIGN",
        "DEPROVISIONING_FROM_CAMPAIGN",
        "PROVISIONING_TO_SMS_PLATFORM",
        "DEPROVISIONING_FROM_SMS_PLATFORM",
        "PROVISIONING_TO_VOICE_PLATFORM",
        "DEPROVISIONING_TO_VOICE_PLATFORM"
    ], StrictStr]] = Field(default=None, alias="eventType")
    status: Optional[StrictStr] = None
    failure_code: Optional[Union[Literal[
        "CAMPAIGN_EXPIRED",
        "CAMPAIGN_MNO_REJECTED",
        "CAMPAIGN_MNO_REVIEW",
        "CAMPAIGN_MNO_SUSPENDED",
        "CAMPAIGN_NOT_AVAILABLE",
        "CAMPAIGN_PENDING_ACCEPTANCE",
        "CAMPAIGN_PROVISIONING_FAILED",
        "EXCEEDED_10DLC_LIMIT",
        "INSUFFICIENT_BALANCE",
        "INVALID_NNID",
        "MNO_SHARING_ERROR",
        "MOCK_CAMPAIGN_NOT_ALLOWED",
        "NUMBER_PROVISIONING_FAILED",
        "PARTNER_SERVICE_UNAVAILABLE",
        "TFN_NOT_ALLOWED"
    ], StrictStr]] = Field(default=None, alias="failureCode")
