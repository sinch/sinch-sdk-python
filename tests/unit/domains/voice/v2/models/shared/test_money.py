from sinch.domains.voice.models.v2.shared.money import Money


def test_money_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = Money(currency_code="USD", amount="0.0123")

    assert model.currency_code == "USD"
    assert model.amount == "0.0123"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["currencyCode"] == "USD"
    assert alias_dump["amount"] == "0.0123"
