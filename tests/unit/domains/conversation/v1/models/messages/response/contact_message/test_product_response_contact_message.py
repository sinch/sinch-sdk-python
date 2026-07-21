import pytest
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    ProductResponseContactMessage,
)


@pytest.fixture
def product_response_contact_message_data():
    return {
        "product_response_message": {
            "products": [
                {
                    "id": "product ID value",
                    "marketplace": "marketplace value",
                    "quantity": 4,
                    "item_price": 3.14159,
                    "currency": "currency value"
                }
            ],
            "title": "a product response message title value",
            "catalog_id": "catalog id value"
        },
        "reply_to": {
            "message_id": "message id value"
        }
    }


def test_parsing_product_response_contact_message_expects_correct_fields(
    product_response_contact_message_data,
):
    """Test that ProductResponseContactMessage is parsed correctly with all fields."""
    parsed_response = ProductResponseContactMessage.model_validate(
        product_response_contact_message_data
    )

    assert isinstance(parsed_response, ProductResponseContactMessage)
    assert parsed_response.product_response_message is not None
    assert len(parsed_response.product_response_message.products) == 1
    product = parsed_response.product_response_message.products[0]
    assert product.id == "product ID value"
    assert product.marketplace == "marketplace value"
    assert product.quantity == 4
    assert product.item_price == 3.14159
    assert product.currency == "currency value"
    assert parsed_response.product_response_message.title == "a product response message title value"
    assert parsed_response.product_response_message.catalog_id == "catalog id value"
    assert parsed_response.reply_to is not None
