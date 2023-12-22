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
    reason: str
    price: dict
    identity: str
    countryId: str
    verificationTimestamp: str


@dataclass
class ReportVerificationUsingIdentityResponse(SinchBaseModel):
    reference: str
    id: str
    method: str
    status: str


@dataclass
class ReportVerificationUsingIdResponse(SinchBaseModel):
    reference: str
    id: str
    method: str
    status: str


@dataclass
class GetVerificationByReferenceResponse(VerificationResponse):
    reference: str


@dataclass
class GetVerificationByIdResponse(VerificationResponse):
    pass


@dataclass
class GetVerificationByIdentityResponse(VerificationResponse):
    reference: str
