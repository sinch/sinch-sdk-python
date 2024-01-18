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
