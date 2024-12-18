from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.domains.sms.endpoints.batches.send_batch import SendBatchSMSEndpoint


def test_authenticate_method_with_service_plan_id_version_of_sms_api(
    sinch_client_sync_with_service_plan_id,
    empty_http_request
):
    sms_endpoint = SendBatchSMSEndpoint(
        sinch=sinch_client_sync_with_service_plan_id,
        request_data=empty_http_request
    )
    http_transport = HTTPTransportRequests(sinch=sinch_client_sync_with_service_plan_id)
    http_transport.authenticate(endpoint=sms_endpoint, request_data=empty_http_request)

    assert empty_http_request.headers
    assert "Bearer" in empty_http_request.headers["Authorization"]
    assert empty_http_request.headers["Content-Type"] == "application/json"


def test_authenticate_method_with_project_id_version_of_sms_api(
    sinch_client_sync,
    empty_http_request
):
    sms_endpoint = SendBatchSMSEndpoint(
        sinch=sinch_client_sync,
        request_data=empty_http_request,
    )
    http_transport = HTTPTransportRequests(sinch=sinch_client_sync)
    http_transport.authenticate(endpoint=sms_endpoint, request_data=empty_http_request)

    assert empty_http_request.headers
    assert "Bearer" in empty_http_request.headers["Authorization"]
    assert empty_http_request.headers["Content-Type"] == "application/json"
