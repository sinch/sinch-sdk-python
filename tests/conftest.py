# This file that contains fixtures that are shared across all tests in the tests directory.
import os
from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from sinch import SinchClient, SinchClientAsync
from sinch.core.models.base_model import SinchBaseModel, SinchRequestBaseModel
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.authentication.models.authentication import OAuthToken
from sinch.domains.numbers.models.v1.shared.active_number import ActiveNumber


@dataclass
class IntBasedPaginationResponse(SinchBaseModel):
    count: int
    page: int
    page_size: int
    pig_dogs: list


@dataclass
class IntBasedPaginationRequest(SinchRequestBaseModel):
    page: int
    page_size: int = 0


@dataclass
class TokenBasedPaginationResponse(SinchBaseModel):
    pig_dogs: list
    next_page_token: str = None


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
def int_based_pagination_request_data():
    return IntBasedPaginationRequest(
        page=0,
        page_size=2
    )


@pytest.fixture
def first_int_based_pagination_response():
    return IntBasedPaginationResponse(
        count=4,
        page=0,
        page_size=2,
        pig_dogs=["Bartosz", "Piotr"]
    )


@pytest.fixture
def second_int_based_pagination_response():
    return IntBasedPaginationResponse(
        count=4,
        page=1,
        page_size=2,
        pig_dogs=["Walaszek", "Połać"]
    )


@pytest.fixture
def third_int_based_pagination_response():
    return IntBasedPaginationResponse(
        count=4,
        page=2,
        page_size=0,
        pig_dogs=[]
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
def sinch_client_async(
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
        SinchClientAsync(
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

    class MockSinchClient:
        configuration = MockConfiguration()

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