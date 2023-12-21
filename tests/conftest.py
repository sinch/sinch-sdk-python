import os
import pytest
from dataclasses import dataclass

from sinch import Client
from sinch import ClientAsync
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.authentication.models.authentication import OAuthToken
from sinch.core.models.base_model import SinchBaseModel, SinchRequestBaseModel


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
    disable_ssl
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

    if verification_origin:
        sinch_client.configuration.verification_origin = verification_origin

    if disable_ssl:
        sinch_client.configuration.disable_https = True

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
def templates_origin():
    return os.getenv("TEMPLATES_ORIGIN")


@pytest.fixture
def disable_ssl():
    return os.getenv("DISABLE_SSL")


@pytest.fixture
def phone_number():
    return os.getenv("PHONE_NUMBER")


@pytest.fixture
def origin_phone_number():
    return os.getenv("ORIGIN_PHONE_NUMBER")


@pytest.fixture
def verification_key():
    return os.getenv("VERIFICATION_KEY")


@pytest.fixture
def verification_secret():
    return os.getenv("VERIFICATION_SECRET")


@pytest.fixture
def verification_id():
    return os.getenv("VERIFICATION_ID")


@pytest.fixture
def app_id():
    return os.getenv("APP_ID")


@pytest.fixture
def contact_id():
    return os.getenv("CONTACT_ID")


@pytest.fixture
def empty_project_id():
    return os.getenv("EMPTY_PROJECT_ID")


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
def sms_http_response():
    return HTTPResponse(
        status_code=404,
        body={
            "text":  "Nobody expects the Spanish Inquisition!"
        },
        headers={
            "SAMPLE_HEADER": "test"
        }
    )


@pytest.fixture
def expired_token_http_response():
    return HTTPResponse(
        status_code=401,
        headers={
            "www-authenticate": "Bearer error='invalid_token', error_description='Jwt expired at...'"
        },
        body={}
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
def first_token_based_pagination_response():
    return TokenBasedPaginationResponse(
        pig_dogs=["Walaszek", "Połać"],
        next_page_token="za30%wsze"
    )


@pytest.fixture
def second_token_based_pagination_response():
    return TokenBasedPaginationResponse(
        pig_dogs=["Bartosz", "Piotr"],
        next_page_token=""
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
    numbers_origin,
    conversation_origin,
    templates_origin,
    auth_origin,
    sms_origin,
    verification_origin,
    disable_ssl,
    project_id
):
    return configure_origin(
        Client(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id
        ),
        numbers_origin,
        conversation_origin,
        templates_origin,
        auth_origin,
        sms_origin,
        verification_origin,
        disable_ssl
    )


@pytest.fixture
def sinch_client_async(
    key_id,
    key_secret,
    numbers_origin,
    conversation_origin,
    templates_origin,
    auth_origin,
    sms_origin,
    verification_origin,
    disable_ssl,
    project_id
):
    return configure_origin(
        ClientAsync(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id
        ),
        numbers_origin,
        conversation_origin,
        templates_origin,
        auth_origin,
        sms_origin,
        verification_origin,
        disable_ssl
    )
