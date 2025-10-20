from unittest.mock import Mock
from sinch.core.pagination import (
    IntBasedPaginator,
    TokenBasedPaginator
)


# Helper function to initialize int paginator
def initialize_int_paginator(endpoint_mock, request_data, responses):
    client = Mock()
    
    # Create a mock that returns different responses based on page number
    def mock_request(endpoint):
        page = endpoint.request_data.page
        if page == 0:
            return responses[0]
        elif page == 1:
            return responses[1]
        else:
            return responses[2]
    
    client.configuration.transport.request.side_effect = mock_request
    endpoint_mock.request_data = request_data

    return IntBasedPaginator(sinch=client, endpoint=endpoint_mock)


def test_page_int_iterator_sync_using_manual_pagination(
    first_int_based_pagination_response,
    second_int_based_pagination_response,
    third_int_based_pagination_response,
    int_based_pagination_request_data
):
    int_based_paginator = initialize_int_paginator(
        endpoint_mock=Mock(),
        request_data=int_based_pagination_request_data,
        responses=[
            first_int_based_pagination_response,
            second_int_based_pagination_response,
            third_int_based_pagination_response
        ]
    )
    assert int_based_paginator

    page_counter = 0
    assert int_based_paginator.result.page == page_counter

    # Test first page content
    delivery_reports = int_based_paginator.content()
    assert len(delivery_reports) == 2
    assert delivery_reports[0]["status"] == "Delivered"
    assert delivery_reports[0]["batch_id"] == "01K7YNS82JMYGAKAATHFP0QTB5"
    assert delivery_reports[0]["recipient"] == "34683607594"
    assert delivery_reports[0]["code"] == 0
    assert delivery_reports[0]["type"] == "recipient_delivery_report_sms"
    assert delivery_reports[1]["status"] == "Delivered"
    assert delivery_reports[1]["batch_id"] == "01K7YNFY30DS2KKVQZVBFANHMR"
    assert delivery_reports[1]["recipient"] == "34683607594"
    assert delivery_reports[1]["code"] == 0
    assert delivery_reports[1]["type"] == "recipient_delivery_report_sms"

    while int_based_paginator.has_next_page:
        int_based_paginator = int_based_paginator.next_page()
        page_counter += 1
        
        # Test content for each page
        delivery_reports = int_based_paginator.content()
        if page_counter == 1:
            assert int_based_paginator.result.page == 1
            assert len(delivery_reports) == 2
            assert delivery_reports[0]["status"] == "Dispatched"
            assert delivery_reports[0]["batch_id"] == "01K7YNFY30DS2KKVQZVBFANHMR"
            assert delivery_reports[0]["recipient"] == "34683607595"
            assert delivery_reports[0]["code"] == 401
            assert delivery_reports[0]["type"] == "recipient_delivery_report_sms"
            assert delivery_reports[1]["status"] == "Failed"
            assert delivery_reports[1]["batch_id"] == "01K7YNFY30DS2KKVQZVBFANHMR"
            assert delivery_reports[1]["recipient"] == "34683607596"
            assert delivery_reports[1]["code"] == 402
            assert delivery_reports[1]["type"] == "recipient_delivery_report_sms"

    assert page_counter == 1


def test_page_int_iterator_sync_using_auto_pagination(
    first_int_based_pagination_response,
    second_int_based_pagination_response,
    third_int_based_pagination_response,
    int_based_pagination_request_data
):
    int_based_paginator = initialize_int_paginator(
        endpoint_mock=Mock(),
        request_data=int_based_pagination_request_data,
        responses=[
            first_int_based_pagination_response,
            second_int_based_pagination_response,
            third_int_based_pagination_response
        ]
    )
    assert int_based_paginator

    page_counter = 0
    assert int_based_paginator.result.page == page_counter

    all_delivery_reports = []
    for delivery_report in int_based_paginator.iterator():
        all_delivery_reports.append(delivery_report)
    
    # Should have 4 delivery reports total (2 from page 0, 2 from page 1, 0 from page 2)
    assert len(all_delivery_reports) == 4
    
    # Test first page reports (page 0)
    assert all_delivery_reports[0]["status"] == "Delivered"
    assert all_delivery_reports[0]["batch_id"] == "01K7YNS82JMYGAKAATHFP0QTB5"
    assert all_delivery_reports[0]["recipient"] == "34683607594"
    assert all_delivery_reports[0]["code"] == 0
    assert all_delivery_reports[0]["type"] == "recipient_delivery_report_sms"
    
    assert all_delivery_reports[1]["status"] == "Delivered"
    assert all_delivery_reports[1]["batch_id"] == "01K7YNFY30DS2KKVQZVBFANHMR"
    assert all_delivery_reports[1]["recipient"] == "34683607594"
    assert all_delivery_reports[1]["code"] == 0
    assert all_delivery_reports[1]["type"] == "recipient_delivery_report_sms"
    
    # Test second page reports (page 1)
    assert all_delivery_reports[2]["status"] == "Dispatched"
    assert all_delivery_reports[2]["batch_id"] == "01K7YNFY30DS2KKVQZVBFANHMR"
    assert all_delivery_reports[2]["recipient"] == "34683607595"
    assert all_delivery_reports[2]["code"] == 401
    assert all_delivery_reports[2]["type"] == "recipient_delivery_report_sms"
    
    assert all_delivery_reports[3]["status"] == "Failed"
    assert all_delivery_reports[3]["batch_id"] == "01K7YNFY30DS2KKVQZVBFANHMR"
    assert all_delivery_reports[3]["recipient"] == "34683607596"
    assert all_delivery_reports[3]["code"] == 402
    assert all_delivery_reports[3]["type"] == "recipient_delivery_report_sms"


# Helper function to initialize token paginator
def initialize_token_paginator(endpoint_mock, request_data, responses):
    client = Mock()
    client.configuration.transport.request.side_effect = responses

    endpoint_mock.request_data = request_data

    return TokenBasedPaginator(sinch=client, endpoint=endpoint_mock)


def test_page_token_iterator_sync_using_manual_pagination(
    token_based_pagination_request_data,
    mock_pagination_active_number_responses,
    mock_pagination_expected_phone_numbers_response
):
    """ Test that the pagination iterates correctly through multiple items. """
    token_based_paginator = initialize_token_paginator(
        endpoint_mock=Mock(),
        request_data=token_based_pagination_request_data,
        responses=mock_pagination_active_number_responses
    )
    assert token_based_paginator is not None

    page_counter = 1
    active_numbers_list = []
    reached_last_page = False
    while not reached_last_page:
        active_numbers_list.extend([num.phone_number for num in token_based_paginator.content()])
        if token_based_paginator.has_next_page:
            token_based_paginator = token_based_paginator.next_page()
            page_counter += 1
            assert isinstance(token_based_paginator, TokenBasedPaginator)
        else:
            reached_last_page = True

    assert page_counter == 3
    assert active_numbers_list == mock_pagination_expected_phone_numbers_response


def test_page_token_iterator_sync_using_auto_pagination_expects_iter(
    token_based_pagination_request_data,
    mock_pagination_active_number_responses,
    mock_pagination_expected_phone_numbers_response
):
    """Test that the pagination iterates correctly through multiple items."""
    token_based_paginator = initialize_token_paginator(
            endpoint_mock=Mock(),
            request_data=token_based_pagination_request_data,
            responses=mock_pagination_active_number_responses
    )
    assert token_based_paginator is not None

    active_numbers_list = []
    for number in token_based_paginator.iterator():
        active_numbers_list.append(number.phone_number)

    assert len(active_numbers_list) == len(mock_pagination_expected_phone_numbers_response)
    assert active_numbers_list == mock_pagination_expected_phone_numbers_response
