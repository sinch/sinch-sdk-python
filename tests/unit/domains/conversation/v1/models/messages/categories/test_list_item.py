import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.messages.categories.list.list_item import (  # noqa: E501
    ListItem,
)
from sinch.domains.conversation.models.v1.messages.categories.list.list_item_choice import (  # noqa: E501
    ListItemChoice,
)
from sinch.domains.conversation.models.v1.messages.categories.list.list_item_product import (  # noqa: E501
    ListItemProduct,
)

adapter = TypeAdapter(ListItem)


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({"choice": {"title": "An option"}}, ListItemChoice),
        (
            {"product": {"id": "p1", "marketplace": "shopify"}},
            ListItemProduct,
        ),
    ],
    ids=["choice", "product"],
)
def test_list_item_resolves_each_variant(payload, expected_type):
    """
    Expects each list item variant to resolve from the key it declares.
    """
    assert type(adapter.validate_python(payload)) is expected_type


def test_list_item_resolves_an_unrecognized_item_to_unknown_in_a_response():
    """
    Expects a list item kind added to the API later to be parsed as
    SinchRawResponse instead of failing the whole message.
    """
    payload = {"bundle": {"id": "b1"}}

    with response_parsing_scope():
        item = adapter.validate_python(payload)

    assert isinstance(item, SinchRawResponse)
    assert item.model_dump() == payload
