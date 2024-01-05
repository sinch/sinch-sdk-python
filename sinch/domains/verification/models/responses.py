from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class StartVerificationResponse(SinchBaseModel):
    id: str
    method: str
    sms: dict
    _links: list


@dataclass
class VerificationResponse(SinchBaseModel):
    id: str
    method: str
    status: str
    price: dict
    identity: str
    countryId: str
    verificationTimestamp: str
    reference: str


@dataclass
class ReportVerificationResponse(SinchBaseModel):
    id: str
    reference: str
    method: str
    status: str


@dataclass
class ReportVerificationUsingIdentityResponse(ReportVerificationResponse):
    pass


@dataclass
class ReportVerificationUsingIdResponse(ReportVerificationResponse):
    pass


@dataclass
class GetVerificationByReferenceResponse(VerificationResponse):
    pass


@dataclass
class GetVerificationByIdResponse(VerificationResponse):
    pass


@dataclass
class GetVerificationByIdentityResponse(VerificationResponse):
    pass
