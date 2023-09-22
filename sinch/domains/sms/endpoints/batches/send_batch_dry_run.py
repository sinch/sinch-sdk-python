from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.batches.responses import SendSMSBatchDryRunResponse
from sinch.domains.sms.models.batches.requests import BatchDryRunRequest


class SendBatchSMSDryRunEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/dry_run"
    HTTP_METHOD = HTTPMethod.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: BatchDryRunRequest):
        super(SendBatchSMSDryRunEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id
        )

    def build_query_params(self):
        return {
            "per_recipient": str(self.request_data.per_recipient).lower(),
            "number_of_recipients": self.request_data.number_of_recipients
        }

    def request_body(self):
        self.request_data.per_recipient = None
        self.request_data.number_of_recipients = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse):
        super(SendBatchSMSDryRunEndpoint, self).handle_response(response)
        return SendSMSBatchDryRunResponse(
            number_of_messages=response.body.get("number_of_messages"),
            number_of_recipients=response.body.get("number_of_recipients"),
            per_recipient=response.body.get("per_recipient")
        )
