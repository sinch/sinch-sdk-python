from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication


def test_sms_endpoint_service_plan_id_credentials_processing(sinch_client_sync_with_service_plan_id, service_plan_id):
    sms_endpoint = SMSEndpoint(
        sinch=sinch_client_sync_with_service_plan_id,
        request_data={}
    )
    assert sms_endpoint.project_or_service_id == service_plan_id
    assert sms_endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.SMS_TOKEN.value
    assert (
        sms_endpoint.sms_origin == sinch_client_sync_with_service_plan_id.configuration._sms_origin_with_service_plan_id
    )


def test_sms_endpoint_with_project_id_credentials_processing(sinch_client_sync, project_id):
    sms_endpoint = SMSEndpoint(
        sinch=sinch_client_sync,
        request_data={}
    )
    assert sms_endpoint.project_or_service_id == project_id
    assert sms_endpoint.sms_origin == sinch_client_sync.configuration.sms_origin
