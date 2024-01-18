from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.verification.enums import VerificationMethod


@dataclass
class StartVerificationResponse(SinchBaseModel):
    id: str
    method: VerificationMethod
    sms: dict
    _links: list


@dataclass
class VerificationResponse(SinchBaseModel):
    id: str
    method: VerificationMethod
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
    method: VerificationMethod
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
