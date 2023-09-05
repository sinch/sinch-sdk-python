from sinch.domains.numbers.models.available.responses import RentAnyNumberResponse


def test_rent_any_number_happy_path(sinch_client_sync):
    numbers_response = sinch_client_sync.numbers.available.rent_any(
        region_code="US",
        type_="LOCAL"
    )
    assert isinstance(numbers_response, RentAnyNumberResponse)


async def test_rent_any_number_happy_path_async(sinch_client_async):
    numbers_response = await sinch_client_async.numbers.available.rent_any(
        region_code="US",
        type_="LOCAL"
    )
    assert isinstance(numbers_response, RentAnyNumberResponse)
