from sinch.core.enums import HTTPAuthentication, HTTPMethods
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
        super().__init__(
            project_id, request_data, response_model=InboundMessage
        )


class ListInboundsEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/inbounds"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS: set = {
        "page",
        "page_size",
        "start_date",
        "end_date",
        "client_reference",
    }

    QUERY_PARAM_FIELDS_EXPLODE_FALSE: set = {"to"}

    def __init__(
        self,
        project_id: str,
        request_data: ListInboundsRequest,
        response_model=ListInboundsResponse,
    ):
        super().__init__(
            project_id, request_data, response_model=response_model
        )
