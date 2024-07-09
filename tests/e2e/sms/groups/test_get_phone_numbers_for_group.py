from sinch.domains.sms.models.groups.responses import SinchGetSMSGroupPhoneNumbersResponse
from sinch.core.enums import HTTPAuthentication

def test_get_group_phone_numbers_sms(sinch_client_sync):
    list_group_response = sinch_client_sync.sms.groups.list()

    get_group_response = sinch_client_sync.sms.groups.get_group_phone_numbers(
        group_id=list_group_response.result.groups[0].id
    )

    assert isinstance(get_group_response, SinchGetSMSGroupPhoneNumbersResponse)
    assert get_group_response.phone_numbers


async def test_get_group_phone_numbers_sms_async(sinch_client_async):
    list_group_response = await sinch_client_async.sms.groups.list()

    get_group_response = await sinch_client_async.sms.groups.get_group_phone_numbers(
        group_id=list_group_response.result.groups[0].id
    )

    assert isinstance(get_group_response, SinchGetSMSGroupPhoneNumbersResponse)
    assert get_group_response.phone_numbers
