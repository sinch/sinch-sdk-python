from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.verification.enums import VerificationMethod, VerificationStatus
from typing import Optional


@dataclass
class StartVerificationResponse(SinchBaseModel):
    id: str
    method: VerificationMethod
    _links: list
    sms: Optional[dict] = None
    flash_call: Optional[dict] = None
    callout: Optional[dict] = None
    seamless: Optional[dict] = None


@dataclass
class VerificationResponse(SinchBaseModel):
    id: str
    method: VerificationMethod
    status: VerificationStatus
    price: dict
    identity: str
    country_id: str
    verification_timestamp: str
    reference: str
    reason: str
    call_complete: bool


@dataclass
class ReportVerificationResponse(VerificationResponse):
    pass


@dataclass
class ReportVerificationByIdentityResponse(ReportVerificationResponse):
    pass


@dataclass
class ReportVerificationByIdResponse(ReportVerificationResponse):
    pass


@dataclass
class GetVerificationStatusByReferenceResponse(VerificationResponse):
    pass


@dataclass
class GetVerificationStatusByIdResponse(VerificationResponse):
    pass


@dataclass
class GetVerificationStatusByIdentityResponse(VerificationResponse):
    pass
