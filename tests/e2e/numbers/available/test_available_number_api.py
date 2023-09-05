import pytest

from sinch.domains.numbers.exceptions import NumbersException
from sinch.domains.numbers import Numbers, ListAvailableNumbersResponse, ActivateNumberResponse, \
    CheckNumberAvailabilityResponse


def fetch_available_numbers(sinch_client):
    return sinch_client.numbers.available.list(
        region_code="GB",
        number_type="MOBILE"
    )


def test_list_available_numbers(sinch_client_sync):
    numbers_response = fetch_available_numbers(sinch_client_sync)
    assert isinstance(numbers_response, ListAvailableNumbersResponse)
    assert len(numbers_response.available_numbers) > 0


def test_list_available_numbers_limit_output_size(sinch_client_sync):
    numbers_response = sinch_client_sync.numbers.available.list(
        region_code="US",
        number_type="LOCAL",
        page_size=10
    )
    assert isinstance(numbers_response, ListAvailableNumbersResponse)
    assert len(numbers_response.available_numbers) == 10


async def test_list_available_numbers_limit_output_size_async(sinch_client_async):
    numbers_response = await sinch_client_async.numbers.available.list(
        region_code="US",
        number_type="LOCAL",
        page_size=10
    )
    assert isinstance(numbers_response, ListAvailableNumbersResponse)
    assert len(numbers_response.available_numbers) == 10


def test_list_available_numbers_400_error_code(sinch_client_sync):
    with pytest.raises(NumbersException) as err:
        sinch_client_sync.numbers.available.list(
            region_code="POZNAN",
            number_type="POTATO"
        )
    assert err


async def test_list_available_numbers_with_voice_capabilities_only(sinch_client_async):
    numbers_response = await sinch_client_async.numbers.available.list(
        region_code="US",
        number_type="LOCAL",
        capabilities=["VOICE"]
    )
    assert isinstance(numbers_response, ListAvailableNumbersResponse)
    assert "VOICE" in numbers_response.available_numbers[0].capability


def test_list_available_numbers_using_number_pattern(sinch_client_sync):
    numbers_response = sinch_client_sync.numbers.available.list(
        region_code="US",
        number_type="LOCAL",
        number_pattern="122",
        number_search_pattern="END"
    )
    assert isinstance(numbers_response, ListAvailableNumbersResponse)
    assert "122" in numbers_response.available_numbers[0].phone_number


def test_activate_new_number(sinch_client_sync):
    available_numbers = fetch_available_numbers(sinch_client_sync)
    numbers_response = sinch_client_sync.numbers.available.activate(
        phone_number=available_numbers.available_numbers[0].phone_number
    )
    assert isinstance(numbers_response, ActivateNumberResponse)


def test_search_for_specific_phone_number(sinch_client_sync):
    numbers_response = fetch_available_numbers(sinch_client_sync)
    numbers_response = sinch_client_sync.numbers.available.check_availability(
        phone_number=numbers_response.available_numbers[0].phone_number
    )
    assert isinstance(numbers_response, CheckNumberAvailabilityResponse)


async def test_search_for_specific_phone_number_async(sinch_client_async, sinch_client_sync):
    available_numbers = fetch_available_numbers(sinch_client_sync)
    numbers_response = await sinch_client_async.numbers.available.check_availability(
        available_numbers.available_numbers[0].phone_number
    )
    assert isinstance(numbers_response, CheckNumberAvailabilityResponse)


def test_list_available_numbers_using_domain_object(sinch_client_sync):
    numbers_client = Numbers(sinch_client_sync)
    numbers_response = numbers_client.available.list(
        region_code="US",
        number_type="LOCAL"
    )
    assert isinstance(numbers_response, ListAvailableNumbersResponse)
