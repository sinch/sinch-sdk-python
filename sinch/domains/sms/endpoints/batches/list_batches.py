from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.models.batches import Batch
from sinch.domains.sms.models.batches.requests import ListBatchesRequest
from sinch.domains.sms.models.batches.responses import ListSMSBatchesResponse


class ListSMSBatchesEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_or_service_id}/batches"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, request_data: ListBatchesRequest, sinch):
        super().__init__(request_data, sinch)

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(origin=self.sms_origin, project_or_service_id=self.project_or_service_id)

    def build_query_params(self):
        return self.request_data.as_dict()

    def handle_response(self, response: HTTPResponse):
        super(ListSMSBatchesEndpoint, self).handle_response(response)
        return ListSMSBatchesResponse(
            batches=[
                Batch(
                    id=batch.get("id"),
                    to=batch.get("to"),
                    from_=batch.get("from"),
                    body=batch.get("body"),
                    delivery_report=batch.get("delivery_report"),
                    cancelled=batch.get("cancelled"),
                    type=batch.get("type"),
                    campaign_id=batch.get("campaign_id"),
                    created_at=batch.get("created_at"),
                    modified_at=batch.get("modified_at"),
                    send_at=batch.get("send_at"),
                    expire_at=batch.get("expire_at"),
                )
                for batch in response.body["batches"]
            ],
            page=response.body.get("page"),
            page_size=response.body.get("page_size"),
            count=response.body.get("count"),
        )
