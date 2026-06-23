# This file that contains fixtures that are shared across all tests in the tests directory.
import os
from dataclasses import dataclass
from unittest.mock import Mock, MagicMock

import pytest
from typing import Optional
from sinch import SinchClient
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.authentication.models.v1.authentication import OAuthToken
from pydantic import BaseModel
from pydantic import Field, StrictInt

def parse_iso_datetime(iso_string):
    """
    Parse ISO datetime string that may end with 'Z' (UTC indicator).
    Compatible with Python 3.9+ by replacing 'Z' with '+00:00'.
    """
    from datetime import datetime
    if iso_string.endswith('Z'):
        iso_string = iso_string[:-1] + '+00:00'
    return datetime.fromisoformat(iso_string)


class SMSBasePaginationRequest(BaseModel):
    page: Optional[StrictInt] = Field(
        default=None)
    page_size: Optional[StrictInt] = Field(
        default=None)


class TokenBasedPaginationRequest(BaseModel):
    page_size: int
    page_token: str = None


@pytest.fixture
def key_id():
    return "test_key_id"

@pytest.fixture
def key_secret():
    return "test_key_secret"

@pytest.fixture
def project_id():
    return "test_project_id"

@pytest.fixture
def service_plan_id():
    return "test_service_plan_id"

@pytest.fixture
def http_response():
    return HTTPResponse(
        status_code=404,
        body={
            "error": {
                "message": "Nobody expects the Spanish Inquisition!"
            }
        },
        headers={
            "SAMPLE_HEADER": "test"
        }
    )


@pytest.fixture
def auth_token():
    return OAuthToken(
        access_token="test",
        expires_in=3599,
        scope="",
        token_type="bearer"
    )


@pytest.fixture
def auth_token_as_dict():
    return {
        'access_token': "test_token",
        'expires_in': 3599,
        'scope': '',
        'token_type': 'bearer'
    }


@pytest.fixture
def token_based_pagination_request_data():
    return TokenBasedPaginationRequest(
        page_size=1
    )


@pytest.fixture
def sms_pagination_request_data():
    return SMSBasePaginationRequest(
        page=0,
        page_size=2
    )

@pytest.fixture
def sms_pagination_request_data_with_page_and_page_size_none():
    return SMSBasePaginationRequest()


@pytest.fixture
def sinch_client_sync(
    key_id,
    key_secret,
    project_id
):
    return SinchClient(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id
        )

@pytest.fixture
def mock_sinch_client_numbers():
    class MockConfiguration:
        numbers_origin = "https://mock-numbers-api.sinch.com"
        project_id = "test_project_id"
        transport = MagicMock()
        transport.request = MagicMock()

    class MockSinchClient:
        configuration = MockConfiguration()

    return MockSinchClient()


@pytest.fixture
def mock_sinch_client_number_lookup():
    class MockConfiguration:
        number_lookup_origin = "https://lookup.api.sinch.com"
        project_id = "test_project_id"
        transport = MagicMock()
        transport.request = MagicMock()

    class MockSinchClient:
        configuration = MockConfiguration()

    return MockSinchClient()


def _create_mock_sinch_client(**config_kwargs):
    """
    Helper function to create a mock Sinch client with the given configuration.
    """
    from sinch.core.clients.sinch_client_configuration import Configuration
    from sinch.core.ports.http_transport import HTTPTransport
    from sinch.core.token_manager import TokenManager
    
    mock_transport = MagicMock(spec=HTTPTransport)
    mock_transport.request = MagicMock()
    
    mock_token_manager = MagicMock(spec=TokenManager)
    
    default_config = {
        "transport": mock_transport,
        "token_manager": mock_token_manager,
        "project_id": "test_project_id",
        "key_id": "test_key_id",
        "key_secret": "test_key_secret",
    }
    default_config.update(config_kwargs)
    
    config = Configuration(**default_config)
    config._authentication_method = "project_auth"
    
    class MockSinchClient:
        configuration = config

    return MockSinchClient()


@pytest.fixture
def mock_sinch_client_sms():
    return _create_mock_sinch_client(
        service_plan_id="test_service_plan_id",
        sms_region="eu"
    )


@pytest.fixture
def mock_sinch_client_conversation():
    return _create_mock_sinch_client(
        conversation_region="us"
    )


@pytest.fixture
def mock_pagination_active_number_responses():
    return [
        Mock(
            content=[
                Mock(phone_number="+12345678901"),
                Mock(phone_number="+12345678902"),
            ],
            next_page_token="token_1",
        ),
        Mock(
            content=[
                Mock(phone_number="+12345678903"),
                Mock(phone_number="+12345678904"),
            ],
            next_page_token="token_2",
        ),
        Mock(
            content=[Mock(phone_number="+12345678905")],
            next_page_token=None,
        ),
    ]


@pytest.fixture
def mock_pagination_expected_phone_numbers_response():
    return [
        "+12345678901", "+12345678902", "+12345678903", "+12345678904", "+12345678905"
    ]


@pytest.fixture
def mock_sms_pagination_responses():
    return [
        Mock(
            content=[
                Mock(batch_id="01K7YNS82JMYGAKAATHFP0QTB5"),
                Mock(batch_id="01K7YNFY30DS2KKVQZVBFANHMR"),
            ],
            count=4, page=0, page_size=2,
        ),
        Mock(
            content=[
                Mock(batch_id="01K7YNGZ45XW8KKPQRSTUVWXYZ"),
                Mock(batch_id="01K7YNHM67YZ3LMNOPQRSTUVWX"),
            ],
            count=4, page=1, page_size=2,
        ),
        Mock(content=[], count=4, page=2, page_size=0),
    ]


@pytest.fixture
def mock_int_pagination_expected_delivery_reports():
    return [
        "01K7YNS82JMYGAKAATHFP0QTB5",
        "01K7YNFY30DS2KKVQZVBFANHMR",
        "01K7YNGZ45XW8KKPQRSTUVWXYZ",
        "01K7YNHM67YZ3LMNOPQRSTUVWX"
    ]
