from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.verification.enums import VerificationMethod
from sinch.domains.verification.models import VerificationIdentity


class ReportPhoneCallVerificationDataTransformationMixin:
    def as_dict(self):
        request_data = super().as_dict()
        payload = {"method": request_data["method"], "callout": {}}

        if request_data.get("code"):
            payload["callout"]["code"] = request_data["code"]

        return payload


class ReportFlashCallVerificationDataTransformationMixin:
    def as_dict(self):
        request_data = super().as_dict()
        payload = {"method": request_data["method"], "flashCall": {}}

        if request_data.get("cli"):
            payload["flashCall"]["cli"] = request_data["cli"]

        return payload


class ReportSMSVerificationDataTransformationMixin:
    def as_dict(self):
        request_data = super().as_dict()
        payload = {"method": request_data["method"], "sms": {}}

        if request_data.get("code"):
            payload["sms"]["code"] = request_data["code"]

        if request_data.get("cli"):
            payload["sms"]["cli"] = request_data["cli"]

        return payload


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
    dial_timeout: int
    method: str = VerificationMethod.FLASH_CALL.value

    def as_dict(self):
        payload = super().as_dict()
        if payload.get("dial_timeout"):
            payload["flashCallOptions"] = {
                "dialTimeout": payload.pop("dial_timeout")
            }
        return payload


@dataclass
class StartPhoneCallVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.CALLOUT.value


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
class StartDataVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.SEAMLESS.value


@dataclass
class ReportVerificationByIdentityRequest(SinchRequestBaseModel):
    endpoint: str


@dataclass
class ReportVerificationByIdentityAndSMSRequest(
    ReportSMSVerificationDataTransformationMixin,
    ReportVerificationByIdentityRequest
):
    code: str
    cli: str
    method: str = VerificationMethod.SMS.value


@dataclass
class ReportVerificationByIdentityAndFlashCallRequest(
    ReportFlashCallVerificationDataTransformationMixin,
    ReportVerificationByIdentityRequest
):
    cli: str
    method: str = VerificationMethod.FLASH_CALL.value


@dataclass
class ReportVerificationByIdentityAndPhoneCallRequest(
    ReportPhoneCallVerificationDataTransformationMixin,
    ReportVerificationByIdentityRequest
):
    code: str
    method: str = VerificationMethod.CALLOUT.value


@dataclass
class ReportVerificationByIdRequest(SinchRequestBaseModel):
    id: str


@dataclass
class ReportVerificationByIdAndSMSRequest(
    ReportSMSVerificationDataTransformationMixin,
    ReportVerificationByIdRequest
):
    code: str
    cli: str
    method: str = VerificationMethod.SMS.value


@dataclass
class ReportVerificationByIdAndFlashCallRequest(
    ReportFlashCallVerificationDataTransformationMixin,
    ReportVerificationByIdRequest
):
    cli: str
    method: str = VerificationMethod.FLASH_CALL.value


@dataclass
class ReportVerificationByIdAndPhoneCallRequest(
    ReportPhoneCallVerificationDataTransformationMixin,
    ReportVerificationByIdRequest
):
    code: str
    method: str = VerificationMethod.CALLOUT.value


@dataclass
class GetVerificationStatusByReferenceRequest(SinchRequestBaseModel):
    reference: str


@dataclass
class GetVerificationStatusByIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    method: str


@dataclass
class GetVerificationStatusByIdRequest(SinchRequestBaseModel):
    id: str


@dataclass
class ReportVerificationByIdentityRequestLegacy(ReportVerificationByIdentityRequest):
    verification_report_request: dict


@dataclass
class ReportVerificationByIdRequestLegacy(ReportVerificationByIdRequest):
    verification_report_request: dict
