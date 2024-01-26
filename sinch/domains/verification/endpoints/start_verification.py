from copy import deepcopy
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.verification.endpoints.verification_endpoint import VerificationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.verification.enums import VerificationMethod
from sinch.domains.verification.models.requests import StartVerificationRequest
from sinch.domains.verification.models.responses import (
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
        if self.request_data.method == VerificationMethod.SMS.value:
            return StartSMSInitiateVerificationResponse(
                **response.body
            )
        elif self.request_data.method == VerificationMethod.FLASHCALL.value:
            return StartFlashCallInitiateVerificationResponse(
                id=response.body.get("id"),
                method=response.body.get("method"),
                _links=response.body.get("_links"),
                flashcall=response.body.get("flashCall")
            )
        elif self.request_data.method == VerificationMethod.CALLOUT.value:
            return StartCalloutInitiateVerificationResponse(
                **response.body
            )
        elif self.request_data.method == VerificationMethod.SEAMLESS.value:
            return StartDataInitiateVerificationResponse(
                **response.body
            )
