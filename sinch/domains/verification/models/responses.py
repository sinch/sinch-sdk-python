from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.verification.enums import VerificationMethod, VerificationStatus


@dataclass
class StartVerificationResponse(SinchBaseModel):
    id: str
    method: VerificationMethod
    _links: list


@dataclass
class StartSMSInitiateVerificationResponse(StartVerificationResponse):
    sms: dict


@dataclass
class StartFlashCallInitiateVerificationResponse(StartVerificationResponse):
    flash_call: dict


@dataclass
class StartCalloutInitiateVerificationResponse(StartVerificationResponse):
    callout: dict


@dataclass
class StartDataInitiateVerificationResponse(StartVerificationResponse):
    seamless: dict


@dataclass
class VerificationResponse(SinchBaseModel):
    id: str
    method: VerificationMethod
    status: VerificationStatus
    price: dict
    identity: dict
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
