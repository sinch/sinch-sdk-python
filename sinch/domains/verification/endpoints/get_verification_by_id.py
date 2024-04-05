from sinch.core.deserializers import timestamp_to_datetime_in_utc_deserializer
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.verification.endpoints.verification_endpoint import VerificationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.verification.models.requests import GetVerificationStatusByIdRequest
from sinch.domains.verification.models.responses import GetVerificationStatusByIdResponse


class GetVerificationStatusByIdEndpoint(VerificationEndpoint):
    ENDPOINT_URL = "{origin}/verification/v1/verifications/id/{id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: GetVerificationStatusByIdRequest):
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.verification_origin,
            id=self.request_data.id
        )

    def handle_response(self, response: HTTPResponse) -> GetVerificationStatusByIdResponse:
        super().handle_response(response)
        return GetVerificationStatusByIdResponse(
            id=response.body.get("id"),
            method=response.body.get("method"),
            status=response.body.get("status"),
            price=response.body.get("price"),
            identity=response.body.get("identity"),
            country_id=response.body.get("countryId"),
            verification_timestamp=timestamp_to_datetime_in_utc_deserializer(
                response.body.get("verificationTimestamp")
            ),
            reference=response.body.get("reference"),
            reason=response.body.get("reason"),
            call_complete=response.body.get("callComplete")
        )
