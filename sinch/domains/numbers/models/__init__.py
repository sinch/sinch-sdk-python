from dataclasses import dataclass
from decimal import Decimal
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.numbers.enums import NumberType, NumberCapability


@dataclass
class Number(SinchBaseModel):
    phone_number: str
    region_code: str
    type: NumberType
    capability: NumberCapability
    setup_price: dict
    monthly_price: dict
    payment_interval_months: int
    supporting_documentation_required: bool


@dataclass
class ScheduledVoiceProvisioning(SinchBaseModel):
    app_id: str
    status: str
    last_updated_time: str


@dataclass
class VoiceConfiguration(SinchBaseModel):
    app_id: str
    scheduled_provisioning: ScheduledVoiceProvisioning


@dataclass
class SmsConfiguration(SinchBaseModel):
    service_plan_id: str
    scheduled_provisioning: ScheduledVoiceProvisioning


@dataclass
class Money(SinchBaseModel):
    currency_code: str
    amount: Decimal
