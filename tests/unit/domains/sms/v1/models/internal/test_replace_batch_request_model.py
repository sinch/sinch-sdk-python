import pytest
from pydantic import TypeAdapter

from sinch.domains.sms.models.v1.internal.replace_batch_request import (
    ReplaceBatchRequest,
    ReplaceBinaryRequest,
    ReplaceMediaRequest,
    ReplaceTextRequest,
)

adapter = TypeAdapter(ReplaceBatchRequest)

BATCH = {"batch_id": "01FC66621XXXXX119Z8PMV1QPQ", "to": ["+12017777777"]}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({**BATCH, "body": "Hello"}, ReplaceTextRequest),
        (
            {**BATCH, "body": "SGVsbG8=", "udh": "06050423F4"},
            ReplaceBinaryRequest,
        ),
        (
            {**BATCH, "body": {"url": "https://example.com/image.jpg"}},
            ReplaceMediaRequest,
        ),
        ({**BATCH, "body": "Hello", "type": "mt_text"}, ReplaceTextRequest),
        (
            {
                **BATCH,
                "body": "SGVsbG8=",
                "udh": "06050423F4",
                "type": "mt_binary",
            },
            ReplaceBinaryRequest,
        ),
        (
            {
                **BATCH,
                "body": {"url": "https://example.com/image.jpg"},
                "type": "mt_media",
            },
            ReplaceMediaRequest,
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
def test_replace_batch_request_union_resolves_each_variant(
    payload, expected_type
):
    """
    Expects each replace variant to resolve from its own fields, and an
    explicit type to resolve to the same variant those fields point to.
    """
    assert type(adapter.validate_python(payload)) is expected_type


@pytest.mark.parametrize("message_type", ["mt_binary", "mt_future"])
def test_replace_batch_request_union_resolves_by_fields_when_the_type_fits_no_variant(
    message_type,
):
    """
    Expects a type whose variant the payload does not fit, or a type the SDK
    does not know, to resolve by the payload's fields and keep that type.
    """
    request = adapter.validate_python(
        {**BATCH, "body": "Hello", "type": message_type}
    )

    assert type(request) is ReplaceTextRequest
    assert request.type == message_type
