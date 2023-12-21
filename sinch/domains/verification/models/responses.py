from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class StartVerificationResponse(SinchBaseModel):
    id: str
    method: str
    sms: dict
    _links: list


@dataclass
class ReportVerificationUsingIdentityResponse(SinchBaseModel):
    pass


@dataclass
class ReportVerificationUsingIdResponse(SinchBaseModel):
    pass


@dataclass
class GetVerificationResponse(SinchBaseModel):
    id: str
    method: str
    status: str
    reason: str
    price: dict
    identity: str
    countryId: str
    verificationTimestamp: str


@dataclass
class GetVerificationByReferenceResponse(GetVerificationResponse):
    pass


@dataclass
class GetVerificationByIdResponse(GetVerificationResponse):
    pass


@dataclass
class GetVerificationByIdentityResponse(GetVerificationResponse):
    pass
