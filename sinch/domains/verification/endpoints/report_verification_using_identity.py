from sinch.core.models.http_response import HTTPResponse
from sinch.domains.verification.endpoints.verification_endpoint import VerificationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.verification.models.requests import ReportVerificationUsingIdentityRequest
from sinch.domains.verification.models.responses import ReportVerificationUsingIdentityResponse


class ReportVerificationUsingIdentityEndpoint(VerificationEndpoint):
    ENDPOINT_URL = "{origin}/verification/v1/verifications/number/{endpoint]"
    HTTP_METHOD = HTTPMethods.PUT.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: ReportVerificationUsingIdentityRequest):
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.verification_origin,
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> ReportVerificationUsingIdentityResponse:
        return ReportVerificationUsingIdentityResponse(
            **response.body
        )
