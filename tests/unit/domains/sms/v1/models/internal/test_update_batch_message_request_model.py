import pytest
from pydantic import TypeAdapter

from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
    UpdateBatchMessageRequest,
    UpdateBinaryRequestWithBatchId,
    UpdateMediaRequestWithBatchId,
    UpdateTextRequestWithBatchId,
)

adapter = TypeAdapter(UpdateBatchMessageRequest)

BATCH = {"batch_id": "01FC66621XXXXX119Z8PMV1QPQ"}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({**BATCH, "body": "Hello"}, UpdateTextRequestWithBatchId),
        (
            {**BATCH, "body": "SGVsbG8=", "udh": "06050423F4"},
            UpdateBinaryRequestWithBatchId,
        ),
        (
            {**BATCH, "body": {"url": "https://example.com/image.jpg"}},
            UpdateMediaRequestWithBatchId,
        ),
        (
            {**BATCH, "body": "Hello", "type": "mt_text"},
            UpdateTextRequestWithBatchId,
        ),
        (
            {
                **BATCH,
                "body": "SGVsbG8=",
                "udh": "06050423F4",
                "type": "mt_binary",
            },
            UpdateBinaryRequestWithBatchId,
        ),
        (
            {
                **BATCH,
                "body": {"url": "https://example.com/image.jpg"},
                "type": "mt_media",
            },
            UpdateMediaRequestWithBatchId,
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
def test_update_batch_message_request_union_resolves_each_variant(
    payload, expected_type
):
    """
    Expects each update variant to resolve from its own fields, and an explicit
    type to resolve to the same variant those fields point to.
    """
    assert type(adapter.validate_python(payload)) is expected_type


def test_update_batch_message_request_union_resolves_an_unknown_type_by_fields():
    """
    Expects a type the SDK does not know to resolve by the payload's fields and
    keep that type.
    """
    request = adapter.validate_python(
        {**BATCH, "body": "Hello", "type": "mt_future"}
    )

    assert type(request) is UpdateTextRequestWithBatchId
    assert request.type == "mt_future"
