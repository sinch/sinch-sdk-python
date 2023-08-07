from sinch.domains.numbers.models.available.responses import RentAnyNumberResponse


def test_rent_any_number_happy_path(sinch_client_sync):
    numbers_response = sinch_client_sync.numbers.available.rent_any(
        region_code="GB",
        type_="LOCAL"
    )
    assert isinstance(numbers_response, RentAnyNumberResponse)
