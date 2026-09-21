from unittest.mock import Mock
import pytest
from sinch.core.pagination import (
    LinkBasedPaginator,
    SMSPaginator,
    TokenBasedPaginator
)
from tests.conftest import SMSBasePaginationRequest


# Helper function to initialize SMS paginator
def initialize_sms_paginator(endpoint_mock, request_data, responses):
    client = Mock()

    # Create a mock that returns different responses based on page number
    def mock_request(endpoint):
        page = endpoint.request_data.page or 0
        if page == 0:
            return responses[0]
        elif page == 1:
            return responses[1]
        else:
            return responses[2]

    client.configuration.transport.request.side_effect = mock_request
    endpoint_mock.request_data = request_data

    return SMSPaginator._initialize(sinch=client, endpoint=endpoint_mock)

def test_page_size_is_zero():
    request_data = SMSBasePaginationRequest(page=0)
    response = Mock(count=0, page=0, page_size=0, content=[])
    client = Mock()
    client.configuration.transport.request.return_value = response
    endpoint = Mock(request_data=request_data)

    paginator = SMSPaginator._initialize(sinch=client, endpoint=endpoint)

    assert paginator.has_next_page is False

def test_response_without_page_size():
    request_data = SMSBasePaginationRequest(page=0)
    response = Mock(count=1, page=0, page_size=None, content=[Mock()])
    client = Mock()
    client.configuration.transport.request.return_value = response
    endpoint = Mock(request_data=request_data)

    paginator = SMSPaginator._initialize(sinch=client, endpoint=endpoint)

    assert paginator.has_next_page is False


def test_partial_last_page_does_not_trigger_extra_call():
    """Regression: when the last page is partial (response.page_size smaller than
    the first response's page_size), the paginator must not request a further
    empty page after the last real one."""
    request_data = SMSBasePaginationRequest()
    responses_by_page = {
        None: Mock(content=[Mock()] * 30, count=49, page=0, page_size=30),
        1: Mock(content=[Mock()] * 19, count=49, page=1, page_size=19),
    }
    client = Mock()
    client.configuration.transport.request.side_effect = (
        lambda ep: responses_by_page[ep.request_data.page]
    )
    endpoint = Mock(request_data=request_data)

    paginator = SMSPaginator._initialize(sinch=client, endpoint=endpoint)
    list(paginator.iterator())

    assert client.configuration.transport.request.call_count == 2

def test_stop_on_first_page():
    """Regression: when the first page is already the last one, the paginator must not make an extra call."""
    request_data = SMSBasePaginationRequest()
    responses_by_page = {
        None: Mock(content=[Mock()] * 15, count=15, page=0, page_size=15),
    }
    client = Mock()
    client.configuration.transport.request.side_effect = (
        lambda ep: responses_by_page[ep.request_data.page]
    )
    endpoint = Mock(request_data=request_data)

    paginator = SMSPaginator._initialize(sinch=client, endpoint=endpoint)
    list(paginator.iterator())

    assert client.configuration.transport.request.call_count == 1


def test_explicit_page_size_with_mid_stream_start_stops_in_one_call():
    """When page_size is passed explicitly and (page+1)*page_size >= count, the
    paginator must stop without making an extra empty call."""
    request_data = SMSBasePaginationRequest(page=1, page_size=30)
    response = Mock(content=[Mock()] * 19, count=49, page=1, page_size=19)
    client = Mock()
    client.configuration.transport.request.return_value = response
    endpoint = Mock(request_data=request_data)

    paginator = SMSPaginator._initialize(sinch=client, endpoint=endpoint)

    assert paginator.has_next_page is False
    assert client.configuration.transport.request.call_count == 1


def test_mid_stream_without_page_size_makes_one_extra_call():
    """Known edge case: starting mid-stream without an explicit page_size can't
    distinguish a partial last page from a full small page, so the paginator
    makes one extra (empty) request before stopping. This test documents the
    inevitable behavior so future changes don't accidentally break it."""
    request_data = SMSBasePaginationRequest(page=1)
    responses_by_page = {
        1: Mock(content=[Mock()] * 19, count=49, page=1, page_size=19),
        2: Mock(content=[], count=49, page=2, page_size=0),
    }
    client = Mock()
    client.configuration.transport.request.side_effect = (
        lambda ep: responses_by_page[ep.request_data.page]
    )
    endpoint = Mock(request_data=request_data)

    paginator = SMSPaginator._initialize(sinch=client, endpoint=endpoint)
    list(paginator.iterator())

    assert client.configuration.transport.request.call_count == 2



def test_page_sms_iterator_sync_using_manual_pagination(
    sms_pagination_request_data,
    mock_sms_pagination_responses,
    mock_int_pagination_expected_delivery_reports
):
    """Test that the pagination iterates correctly through multiple items."""
    sms_paginator = initialize_sms_paginator(
        endpoint_mock=Mock(),
        request_data=sms_pagination_request_data,
        responses=mock_sms_pagination_responses
    )
    assert sms_paginator is not None

    page_counter = 0
    assert sms_paginator.result.page == page_counter

    delivery_reports_list = []
    reached_last_page = False
    while not reached_last_page:
        delivery_reports_list.extend([report.batch_id for report in sms_paginator.content()])
        if sms_paginator.has_next_page:
            sms_paginator = sms_paginator.next_page()
            page_counter += 1
            assert isinstance(sms_paginator, SMSPaginator)
        else:
            reached_last_page = True

    assert page_counter == 1
    assert delivery_reports_list == mock_int_pagination_expected_delivery_reports


def test_page_sms_iterator_sync_using_auto_pagination(
    sms_pagination_request_data,
    mock_sms_pagination_responses,
    mock_int_pagination_expected_delivery_reports
):
    """Test that the pagination iterates correctly through multiple items."""
    sms_paginator = initialize_sms_paginator(
        endpoint_mock=Mock(),
        request_data=sms_pagination_request_data,
        responses=mock_sms_pagination_responses
    )
    assert sms_paginator is not None

    page_counter = 0
    assert sms_paginator.result.page == page_counter

    all_delivery_reports = []
    for delivery_report in sms_paginator.iterator():
        all_delivery_reports.append(delivery_report.batch_id)

    # Should have 4 delivery reports total (2 from page 0, 2 from page 1, 0 from page 2)
    assert len(all_delivery_reports) == 4
    assert all_delivery_reports == mock_int_pagination_expected_delivery_reports


# Helper function to initialize token paginator
def initialize_token_paginator(endpoint_mock, request_data, responses):
    client = Mock()
    client.configuration.transport.request.side_effect = responses

    endpoint_mock.request_data = request_data

    return TokenBasedPaginator._initialize(sinch=client, endpoint=endpoint_mock)


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


# Link based pagination, as defined by the Sinch REST API standards: the next page is addressed
# by an absolute link served by the API instead of a token echoed back into the query parameters.

NEXT_PAGE_LINK = "https://contacts.api.sinch.com/v1/projects/proj/contacts?pageToken=cursor-def"


def initialize_link_paginator(responses):
    """Builds a LinkBasedPaginator serving the given responses in order."""
    client = Mock()
    client.configuration.transport.request.side_effect = list(responses)
    endpoint = Mock()

    return LinkBasedPaginator._initialize(sinch=client, endpoint=endpoint), client


def page_with_next_link(*items):
    return Mock(content=list(items), links=Mock(next=NEXT_PAGE_LINK))


def last_page(*items):
    return Mock(content=list(items), links=Mock(next=None))


def test_link_based_announces_next_page_while_a_link_is_served():
    paginator, _ = initialize_link_paginator([page_with_next_link(Mock(), Mock())])

    assert paginator.has_next_page is True
    assert len(paginator.content()) == 2


def test_link_based_requests_the_next_page_from_the_served_link():
    """The next page has to be fetched from the link, not rebuilt from the query parameters."""
    paginator, client = initialize_link_paginator(
        [page_with_next_link(Mock()), last_page(Mock())]
    )

    paginator.next_page()

    next_endpoint = client.configuration.transport.request.call_args[0][0]
    assert next_endpoint.build_url(Mock()) == NEXT_PAGE_LINK
    assert next_endpoint.build_query_params() == {}


def test_link_based_delegates_everything_but_the_url_to_the_paginated_endpoint():
    paginator, client = initialize_link_paginator(
        [page_with_next_link(Mock()), last_page(Mock())]
    )
    endpoint = paginator.endpoint

    paginator.next_page()

    next_endpoint = client.configuration.transport.request.call_args[0][0]
    assert next_endpoint.HTTP_METHOD == endpoint.HTTP_METHOD
    assert next_endpoint.HTTP_AUTHENTICATION == endpoint.HTTP_AUTHENTICATION


def test_link_based_stops_when_no_next_link_is_served():
    paginator, _ = initialize_link_paginator(
        [page_with_next_link(Mock()), last_page(Mock())]
    )

    last = paginator.next_page()

    assert last.has_next_page is False
    assert last.next_page() is None


def test_link_based_stops_when_no_links_object_is_served():
    """The standards allow the links object to be omitted when the collection fits in a page."""
    paginator, _ = initialize_link_paginator([Mock(content=[Mock()], links=None)])

    assert paginator.has_next_page is False


def test_link_based_iterator_walks_every_page_on_demand():
    paginator, client = initialize_link_paginator(
        [page_with_next_link(Mock(), Mock()), last_page(Mock())]
    )

    items = list(paginator.iterator())

    assert len(items) == 3
    assert client.configuration.transport.request.call_count == 2
