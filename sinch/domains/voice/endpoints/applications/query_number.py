from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.applications.requests import QueryNumberVoiceApplicationRequest
from sinch.domains.voice.models.applications.responses import QueryNumberVoiceApplicationResponse


class QueryVoiceNumberEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v1/calling/query/number/{number}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: QueryNumberVoiceApplicationRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_applications_origin, number=self.request_data.number
        )

    def handle_response(self, response: HTTPResponse) -> QueryNumberVoiceApplicationResponse:
        super().handle_response(response)
        return QueryNumberVoiceApplicationResponse(
            country_id=response.body["number"]["countryId"],
            number_type=response.body["number"]["numberType"],
            normalized_number=response.body["number"]["normalizedNumber"],
            restricted=response.body["number"]["restricted"],
            rate=response.body["number"]["rate"],
        )
