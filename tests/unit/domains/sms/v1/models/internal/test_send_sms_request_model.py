import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.sms.models.v1.internal.send_sms_request import (
    SendSMSRequest,
)
from sinch.domains.sms.models.v1.shared.binary_request import BinaryRequest
from sinch.domains.sms.models.v1.shared.media_request import MediaRequest
from sinch.domains.sms.models.v1.shared.text_request import TextRequest

adapter = TypeAdapter(SendSMSRequest)


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({"to": ["+12017777777"], "body": "Hello"}, TextRequest),
        (
            {"to": ["+12017777777"], "body": "SGVsbG8=", "udh": "06050423F4"},
            BinaryRequest,
        ),
        (
            {
                "to": ["+12017777777"],
                "body": {"url": "https://example.com/image.jpg"},
            },
            MediaRequest,
        ),
        (
            {"to": ["+12017777777"], "body": "Hello", "type": "mt_text"},
            TextRequest,
        ),
        (
            {
                "to": ["+12017777777"],
                "body": "SGVsbG8=",
                "udh": "06050423F4",
                "type": "mt_binary",
            },
            BinaryRequest,
        ),
        (
            {
                "to": ["+12017777777"],
                "body": {"url": "https://example.com/image.jpg"},
                "type": "mt_media",
            },
            MediaRequest,
        ),
    ],
    ids=[
        "text_without_type",
        "binary_without_type",
        "media_without_type",
        "text_with_type",
        "binary_with_type",
        "media_with_type",
    ],
)
def test_send_sms_request_union_resolves_each_variant(payload, expected_type):
    """
    Expects each request variant to resolve from its own fields, and an
    explicit type to resolve to the same variant those fields point to.
    """
    assert type(adapter.validate_python(payload)) is expected_type


@pytest.mark.parametrize("message_type", ["mt_binary", "mt_future"])
def test_send_sms_request_union_resolves_by_fields_when_the_type_fits_no_variant(
    message_type,
):
    """
    Expects a type whose variant the payload does not fit, or a type the SDK
    does not know, to resolve by the payload's fields and keep that type.
    """
    request = adapter.validate_python(
        {"to": ["+12017777777"], "body": "Hello", "type": message_type}
    )

    assert type(request) is TextRequest
    assert request.type == message_type


def test_send_sms_request_union_rejects_a_payload_matching_no_variant():
    """
    Expects a payload no variant accepts to raise pydantic's own union error.
    """
    with pytest.raises(ValidationError, match="body"):
        adapter.validate_python({"to": ["+12017777777"]})


def test_send_sms_request_union_keeps_an_already_built_request():
    """
    Expects a request the caller built to be kept as it is.
    """
    request = BinaryRequest(
        to=["+12017777777"], body="SGVsbG8=", udh="06050423F4"
    )
    assert adapter.validate_python(request) is not None
    assert type(adapter.validate_python(request)) is BinaryRequest
