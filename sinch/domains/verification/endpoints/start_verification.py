from sinch.core.models.http_response import HTTPResponse
from sinch.domains.verification.endpoints.verification_endpoint import VerificationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.verification.enums import VerificationMethod
from sinch.domains.verification.models.requests import StartVerificationRequest
from sinch.domains.verification.models.responses import (
    FlashCallResponse,
    SMSResponse,
    DataResponse,
    StartVerificationResponse,
    StartSMSInitiateVerificationResponse,
    StartDataInitiateVerificationResponse,
    StartCalloutInitiateVerificationResponse,
    StartFlashCallInitiateVerificationResponse
)


class StartVerificationEndpoint(VerificationEndpoint):
    ENDPOINT_URL = "{origin}/verification/v1/verifications"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: StartVerificationRequest):
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.verification_origin,
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> StartVerificationResponse:
        super().handle_response(response)
        if self.request_data.method == VerificationMethod.SMS.value:
            sms_response = response.body.get("sms")
            return StartSMSInitiateVerificationResponse(
                id=response.body.get("id"),
                method=response.body.get("method"),
                _links=response.body.get("_links"),
                sms=SMSResponse(
                    interception_timeout=response.body["sms"].get("interceptionTimeout"),
                    template=response.body["sms"].get("template")
                ) if sms_response else None
            )
        elif self.request_data.method == VerificationMethod.FLASH_CALL.value:
            flash_call_response = response.body.get("flashCall")
            return StartFlashCallInitiateVerificationResponse(
                id=response.body.get("id"),
                method=response.body.get("method"),
                _links=response.body.get("_links"),
                flash_call=FlashCallResponse(
                    cli_filter=response.body["flashCall"].get("cliFilter"),
                    interception_timeout=response.body["flashCall"].get("interceptionTimeout"),
                    report_timeout=response.body["flashCall"].get("reportTimeout"),
                    deny_call_after=response.body["flashCall"].get("denyCallAfter")
                ) if flash_call_response else None
            )
        elif self.request_data.method == VerificationMethod.CALLOUT.value:
            return StartCalloutInitiateVerificationResponse(
                id=response.body.get("id"),
                method=response.body.get("method"),
                _links=response.body.get("_links")
            )
        elif self.request_data.method == VerificationMethod.SEAMLESS.value:
            seamless_response = response.body.get("seamless")
            return StartDataInitiateVerificationResponse(
                id=response.body.get("id"),
                method=response.body.get("method"),
                _links=response.body.get("_links"),
                seamless=DataResponse(
                    target_uri=response.body["seamless"].get("targetUri")
                ) if seamless_response else None
            )
