from sinch.core.models.http_response import HTTPResponse
from sinch.domains.verification.endpoints.verification_endpoint import VerificationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.verification.models.requests import GetVerificationStatusByIdentityRequest
from sinch.domains.verification.models.responses import GetVerificationStatusByIdentityResponse


class GetVerificationStatusByIdentityEndpoint(VerificationEndpoint):
    ENDPOINT_URL = "{origin}/verification/v1/verifications/{method}/number/{endpoint}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: GetVerificationStatusByIdentityRequest):
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.verification_origin,
            method=self.request_data.method,
            endpoint=self.request_data.endpoint
        )

    def handle_response(self, response: HTTPResponse) -> GetVerificationStatusByIdentityResponse:
        super().handle_response(response)
        return GetVerificationStatusByIdentityResponse(
            id=response.body.get("id"),
            method=response.body.get("method"),
            status=response.body.get("status"),
            price=response.body.get("price"),
            identity=response.body.get("identity"),
            country_id=response.body.get("country_id"),
            verification_timestamp=response.body.get("verification_timestamp"),
            reference=response.body.get("reference"),
            reason=response.body.get("reason"),
            call_complete=response.body.get("call_complete")
        )
