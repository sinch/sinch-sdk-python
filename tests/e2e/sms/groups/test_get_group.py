from sinch.domains.sms.models.groups.responses import GetSMSGroupResponse
from sinch.core.enums import HTTPAuthentication


def test_get_sms_group_with_service_plan_id(sinch_client_sync):
    sinch_client_sync.configuration.sms_authentication_method = HTTPAuthentication.SMS_TOKEN.value
    list_group_response = sinch_client_sync.sms.groups.list()

    get_group_response = sinch_client_sync.sms.groups.get(
        group_id=list_group_response.result.groups[0].id
    )
    assert isinstance(get_group_response, GetSMSGroupResponse)


def test_get_sms_group(sinch_client_sync):
    list_group_response = sinch_client_sync.sms.groups.list()

    get_group_response = sinch_client_sync.sms.groups.get(
        group_id=list_group_response.result.groups[0].id
    )
    assert isinstance(get_group_response, GetSMSGroupResponse)


async def test_get_sms_group_async(sinch_client_async):
    list_group_response = await sinch_client_async.sms.groups.list()

    get_group_response = await sinch_client_async.sms.groups.get(
        group_id=list_group_response.result.groups[0].id
    )
    assert isinstance(get_group_response, GetSMSGroupResponse)
