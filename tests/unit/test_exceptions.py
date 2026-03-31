from sinch.core.exceptions import ValidationException
from sinch.domains.numbers.api.v1.exceptions import NumbersException
from sinch.domains.conversation.exceptions import ConversationException
from sinch.domains.sms.exceptions import SMSException
from sinch.domains.authentication.exceptions import AuthenticationException


def test_sinch_validation_exception_not_from_remote_server():
    try:
        raise ValidationException(
            is_from_server=False,
            message="ValidationFailure",
            response=None
        )
    except ValidationException as error:
        assert not error.is_from_server
        assert str(error) == "ValidationFailure"
        assert error.response_status_code is None
        assert error.http_response is None


def test_sinch_numbers_exception_from_server(http_response):
    try:
        raise NumbersException(
            is_from_server=True,
            message="NumbersFailure",
            response=http_response
        )
    except NumbersException as error:
        assert error.is_from_server
        assert str(error) == "NumbersFailure"
        assert error.response_status_code is http_response.status_code
        assert error.http_response == http_response


def test_sinch_conversation_exception_from_server(http_response):
    try:
        raise ConversationException(
            is_from_server=True,
            message="ConversationAPIFailure",
            response=http_response
        )
    except ConversationException as error:
        assert error.is_from_server
        assert str(error) == "ConversationAPIFailure"
        assert error.response_status_code is http_response.status_code
        assert error.http_response == http_response


def test_sinch_sms_exception_from_server(http_response):
    try:
        raise SMSException(
            is_from_server=True,
            message="SMSFailure",
            response=http_response
        )
    except SMSException as error:
        assert error.is_from_server
        assert str(error) == "SMSFailure"
        assert error.response_status_code is http_response.status_code
        assert error.http_response == http_response


def test_sinch_authentication_exception_from_server(http_response):
    try:
        raise AuthenticationException(
            is_from_server=True,
            message="AuthFailure",
            response=http_response
        )
    except AuthenticationException as error:
        assert error.is_from_server
        assert str(error) == "AuthFailure"
        assert error.response_status_code is http_response.status_code
        assert error.http_response == http_response
