from sinch.core.deserializers import timestamp_to_datetime_in_utc_deserializer
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.calls.responses import GetVoiceCallResponse
from sinch.domains.voice.models.calls.requests import GetVoiceCallRequest
from sinch.domains.voice.models import Price, Destination


class GetCallEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/calling/v1/calls/id/{call_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: GetVoiceCallRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_origin,
            call_id=self.request_data.call_id
        )

    def handle_response(self, response: HTTPResponse) -> GetVoiceCallResponse:
        super().handle_response(response)
        call_origin = response.body.get("from")
        call_destination = response.body.get("to")
        return GetVoiceCallResponse(
            from_=Destination(
                type=call_origin["type"],
                endpoint=call_origin.get["endpoint"],
            ) if call_origin else None,
            to=Destination(
                type=call_destination.get("type"),
                endpoint=call_destination.get("endpoint")
            ) if call_destination else None,
            domain=response.body.get("domain"),
            call_id=response.body.get("callId"),
            duration=response.body.get("duration"),
            status=response.body.get("status"),
            result=response.body.get("result"),
            reason=response.body.get("reason"),
            timestamp=timestamp_to_datetime_in_utc_deserializer(response.body["timestamp"]),
            custom=response.body.get("custom"),
            user_rate=Price(
                currency_id=response.body["userRate"]["currencyId"],
                amount=response.body["userRate"]["amount"]
            ),
            debit=Price(
                currency_id=response.body["userRate"]["currencyId"],
                amount=response.body["userRate"]["amount"]
            )
        )
