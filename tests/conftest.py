# This file that contains fixtures that are shared across all tests in the tests directory.
import os
from dataclasses import dataclass
from unittest.mock import Mock, MagicMock
from sinch.domains.sms.models.v1.internal import (
    ListDeliveryReportsRequest,
    ListDeliveryReportsResponse,
)
from sinch.domains.sms.models.v1.response import RecipientDeliveryReport

import pytest

from sinch import SinchClient
from sinch.core.models.base_model import SinchBaseModel, SinchRequestBaseModel
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.authentication.models.v1.authentication import OAuthToken
from sinch.domains.numbers.models.v1.response import ActiveNumber


def parse_iso_datetime(iso_string):
    """
    Parse ISO datetime string that may end with 'Z' (UTC indicator).
    Compatible with Python 3.9+ by replacing 'Z' with '+00:00'.
    """
    from datetime import datetime
    if iso_string.endswith('Z'):
        iso_string = iso_string[:-1] + '+00:00'
    return datetime.fromisoformat(iso_string)


@dataclass
class IntBasedPaginationRequest(SinchRequestBaseModel):
    page: int
    page_size: int = 0


@dataclass
class TokenBasedPaginationRequest(SinchRequestBaseModel):
    page_size: int
    page_token: str = None


def configure_origin(
    sinch_client,
    numbers_origin,
    conversation_origin,
    templates_origin,
    auth_origin,
    sms_origin,
    verification_origin,
    voice_origin
):
    if auth_origin:
        sinch_client.configuration.auth_origin = auth_origin

    if numbers_origin:
        sinch_client.configuration.numbers_origin = numbers_origin

    if conversation_origin:
        sinch_client.configuration.conversation_origin = conversation_origin

    if templates_origin:
        sinch_client.configuration.templates_origin = templates_origin

    if sms_origin:
        sinch_client.configuration.sms_origin = sms_origin
        sinch_client.configuration.sms_origin_with_service_plan_id = sms_origin

    if verification_origin:
        sinch_client.configuration.verification_origin = verification_origin

    if voice_origin:
        sinch_client.configuration.voice_origin = voice_origin
        sinch_client.configuration.voice_applications_origin = voice_origin

    return sinch_client


@pytest.fixture
def key_id():
    return os.getenv("KEY_ID")


@pytest.fixture
def key_secret():
    return os.getenv("KEY_SECRET")


@pytest.fixture
def project_id():
    return os.getenv("PROJECT_ID")


@pytest.fixture
def numbers_origin():
    return os.getenv("NUMBERS_ORIGIN")


@pytest.fixture
def conversation_origin():
    return os.getenv("CONVERSATION_ORIGIN")


@pytest.fixture
def auth_origin():
    return os.getenv("AUTH_ORIGIN")


@pytest.fixture
def sms_origin():
    return os.getenv("SMS_ORIGIN")


@pytest.fixture
def verification_origin():
    return os.getenv("VERIFICATION_ORIGIN")


@pytest.fixture
def voice_origin():
    return os.getenv("VOICE_ORIGIN")


@pytest.fixture
def templates_origin():
    return os.getenv("TEMPLATES_ORIGIN")


@pytest.fixture
def disable_ssl():
    return os.getenv("DISABLE_SSL")


@pytest.fixture
def application_key():
    return os.getenv("APPLICATION_KEY")


@pytest.fixture
def application_secret():
    return os.getenv("APPLICATION_SECRET")


@pytest.fixture
def service_plan_id():
    return os.getenv("SERVICE_PLAN_ID")

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
    return ListDeliveryReportsRequest(
        page=0,
        page_size=2
    )


@pytest.fixture
def third_int_based_pagination_response():
    return ListDeliveryReportsResponse(
        count=4,
        page=2,
        page_size=2,
        delivery_reports=[]
    )


@pytest.fixture
def sinch_client_sync(
    key_id,
    key_secret,
    application_key,
    application_secret,
    numbers_origin,
    conversation_origin,
    templates_origin,
    auth_origin,
    sms_origin,
    verification_origin,
    voice_origin,
    project_id
):
    return configure_origin(
        SinchClient(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id,
            application_key=application_key,
            application_secret=application_secret
        ),
        numbers_origin,
        conversation_origin,
        templates_origin,
        auth_origin,
        sms_origin,
        verification_origin,
        voice_origin
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
def mock_sinch_client_sms():
    from sinch.core.clients.sinch_client_configuration import Configuration
    from sinch.core.ports.http_transport import HTTPTransport
    from sinch.core.token_manager import TokenManager
    
    mock_transport = MagicMock(spec=HTTPTransport)
    mock_transport.request = MagicMock()
    
    mock_token_manager = MagicMock(spec=TokenManager)
    
    config = Configuration(
        transport=mock_transport,
        token_manager=mock_token_manager,
        project_id="test_project_id",
        service_plan_id="test_service_plan_id",
        sms_region="eu"
    )
    
    config._authentication_method = "project_auth"
    
    class MockSinchClient:
        configuration = config

    return MockSinchClient()


@pytest.fixture
def mock_pagination_active_number_responses():
    return [
        Mock(content=[ActiveNumber(phone_number="+12345678901"),
                      ActiveNumber(phone_number="+12345678902")],
             next_page_token="token_1"),
        Mock(content=[ActiveNumber(phone_number="+12345678903"),
                      ActiveNumber(phone_number="+12345678904")],
             next_page_token="token_2"),
        Mock(content=[ActiveNumber(phone_number="+12345678905")],
             next_page_token=None)
    ]


@pytest.fixture
def mock_pagination_expected_phone_numbers_response():
    return [
        "+12345678901", "+12345678902", "+12345678903", "+12345678904", "+12345678905"
    ]


@pytest.fixture
def mock_sms_pagination_responses():
    from datetime import datetime
    from sinch.domains.sms.models.v1.response import RecipientDeliveryReport
    
    return [
        Mock(content=[
            RecipientDeliveryReport(
                at=parse_iso_datetime("2025-10-19T16:45:31.935Z"),
                batch_id="01K7YNS82JMYGAKAATHFP0QTB5",
                code=400,
                recipient="12346836075",
                status="DELIVERED",
                type="recipient_delivery_report_sms"
            ),
            RecipientDeliveryReport(
                at=parse_iso_datetime("2025-10-19T16:40:26.855Z"),
                batch_id="01K7YNFY30DS2KKVQZVBFANHMR",
                code=400,
                recipient="12346836075",
                status="DELIVERED",
                type="recipient_delivery_report_sms"
            )
        ],
             count=4, page=0, page_size=2),
        Mock(content=[
            RecipientDeliveryReport(
                at=parse_iso_datetime("2025-10-19T16:35:15.123Z"),
                batch_id="01K7YNGZ45XW8KKPQRSTUVWXYZ",
                code=401,
                recipient="34683607595",
                status="DISPATCHED",
                type="recipient_delivery_report_sms"
            ),
            RecipientDeliveryReport(
                at=parse_iso_datetime("2025-10-19T16:30:10.456Z"),
                batch_id="01K7YNHM67YZ3LMNOPQRSTUVWX",
                code=402,
                recipient="34683607596",
                status="FAILED",
                type="recipient_delivery_report_sms"
            )
        ],
             count=4, page=1, page_size=2),
        Mock(content=[],
             count=4, page=2, page_size=2)
    ]


@pytest.fixture
def mock_int_pagination_expected_delivery_reports():
    return [
        "01K7YNS82JMYGAKAATHFP0QTB5",
        "01K7YNFY30DS2KKVQZVBFANHMR",
        "01K7YNGZ45XW8KKPQRSTUVWXYZ",
        "01K7YNHM67YZ3LMNOPQRSTUVWX"
    ]
