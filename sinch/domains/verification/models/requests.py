from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.verification.enums import VerificationMethod
from sinch.domains.verification.models import VerificationIdentity


@dataclass
class StartVerificationRequest(SinchRequestBaseModel):
    identity: VerificationIdentity
    reference: str
    custom: str


@dataclass
class StartSMSVerificationRequest(StartVerificationRequest):
    expiry: str
    code_type: str
    template: str
    method: str = VerificationMethod.SMS.value

    def as_dict(self):
        payload = super().as_dict()
        payload["smsOptions"] = {}

        if payload.get("code_type"):
            payload["smsOptions"].update({
                "codeType": payload.pop("code_type")
            })
        elif payload.get("expiry"):
            payload["smsOptions"].update({
                "expiry": payload.pop("expiry")
            })
        elif payload.get("template"):
            payload["smsOptions"].update({
                "template": payload.pop("template")
            })
        return payload


@dataclass
class StartFlashCallVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.FLASH_CALL.value


@dataclass
class StartCalloutVerificationRequest(StartVerificationRequest):
    speech_locale: str
    method: str = VerificationMethod.CALLOUT.value

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("speech_locale"):
            payload["calloutOptions"] = {
                "speech": {
                    "locale": payload.pop("speech_locale")
                }
            }
        return payload


@dataclass
class StartSeamlessVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.SEAMLESS.value


@dataclass
class ReportVerificationByIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    verification_report_request: dict


@dataclass
class ReportVerificationByIdRequest(SinchRequestBaseModel):
    id: str
    verification_report_request: dict


@dataclass
class GetVerificationStatusByReferenceRequest(SinchRequestBaseModel):
    reference: str


@dataclass
class GetVerificationStatusByIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    method: VerificationMethod
