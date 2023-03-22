from sinch.domains.numbers.enums import NumberType
from sinch.domains.numbers.models.responses import ListAvailableRegionsResponse


def test_list_available_regions(sinch_client_sync):
    available_regions_response = sinch_client_sync.numbers.regions.list(
        NumberType.LOCAL.value
    )
    assert isinstance(available_regions_response, ListAvailableRegionsResponse)


def test_list_available_regions_using_types(sinch_client_sync):
    available_regions_response = sinch_client_sync.numbers.regions.list(
        number_types=[NumberType.LOCAL.value, NumberType.MOBILE.value]
    )
    assert isinstance(available_regions_response, ListAvailableRegionsResponse)


async def test_list_available_regions_async(sinch_client_async):
    available_regions_response = await sinch_client_async.numbers.regions.list(
        number_type=NumberType.LOCAL.value
    )
    assert isinstance(available_regions_response, ListAvailableRegionsResponse)
