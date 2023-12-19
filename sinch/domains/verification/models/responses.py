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
class GetVerificationByReferenceResponse(SinchBaseModel):
    pass


@dataclass
class GetVerificationByIdResponse(SinchBaseModel):
    pass


@dataclass
class GetVerificationByIdentityResponse(SinchBaseModel):
    pass
