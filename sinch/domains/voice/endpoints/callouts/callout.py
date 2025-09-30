import json
from sinch.domains.voice.enums import CalloutMethod
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.callouts.responses import VoiceCalloutResponse


class CalloutEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/calling/v1/callouts"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data, callout_method):
        self.request_data = request_data
        self.callout_method = callout_method

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_origin
        )

    def request_body(self):
        request_data = {}
        if self.callout_method == CalloutMethod.TEXT_TO_SPEECH.value:
            request_data["method"] = CalloutMethod.TEXT_TO_SPEECH.value
            request_data[CalloutMethod.TEXT_TO_SPEECH.value] = self.request_data.as_dict()

        elif self.callout_method == CalloutMethod.CUSTOM.value:
            request_data["method"] = CalloutMethod.CUSTOM.value
            request_data[CalloutMethod.CUSTOM.value] = self.request_data.as_dict()

        elif self.callout_method == CalloutMethod.CONFERENCE.value:
            request_data["method"] = CalloutMethod.CONFERENCE.value
            if self.request_data.conferenceDtmfOptions:
                dtmf_options = {}

                if self.request_data.conferenceDtmfOptions["mode"]:
                    dtmf_options["mode"] = self.request_data.conferenceDtmfOptions["mode"]

                if self.request_data.conferenceDtmfOptions["timeout_mills"]:
                    dtmf_options["timeoutMills"] = self.request_data.conferenceDtmfOptions["timeout_mills"]

                if self.request_data.conferenceDtmfOptions["max_digits"]:
                    dtmf_options["maxDigits"] = self.request_data.conferenceDtmfOptions["max_digits"]

                self.request_data.conferenceDtmfOptions = dtmf_options

            request_data[CalloutMethod.CONFERENCE.value] = self.request_data.as_dict()

        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse):
        super().handle_response(response)
        return VoiceCalloutResponse(call_id=response.body["callId"])
