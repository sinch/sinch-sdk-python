from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.utils import model_dump_for_query_params
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.api.v1.internal.base.sms_endpoint import SmsEndpoint
from sinch.domains.sms.models.v1.internal.inbound_id_request import (
    InboundIdRequest,
)
from sinch.domains.sms.models.v1.internal.list_inbounds_request import (
    ListInboundsRequest,
)
from sinch.domains.sms.models.v1.internal.list_inbounds_response import (
    ListInboundsResponse,
)
from sinch.domains.sms.models.v1.types.inbound_message import InboundMessage


class GetInboundEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/inbounds/{inbound_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: InboundIdRequest):
        super(GetInboundEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(self, response: HTTPResponse) -> InboundMessage:
        try:
            super(GetInboundEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, InboundMessage)


class ListInboundsEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/inbounds"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListInboundsRequest):
        super(ListInboundsEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return model_dump_for_query_params(self.request_data)

    def handle_response(self, response: HTTPResponse) -> ListInboundsResponse:
        try:
            super(ListInboundsEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, ListInboundsResponse)
