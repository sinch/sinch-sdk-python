from sinch.domains.conversation.models.v1.sinch_events.contact.duplicated_identities import (
    DuplicatedIdentities,
)


def test_duplicated_identities_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DuplicatedIdentities(channel="SMS", contact_ids=["contact-1", "contact-2"])

    assert model.channel == "SMS"
    assert model.contact_ids == ["contact-1", "contact-2"]

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["channel"] == "SMS"
    assert alias_dump["contact_ids"] == ["contact-1", "contact-2"]


def test_duplicated_identities_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = DuplicatedIdentities()

    assert model.channel is None
    assert model.contact_ids is None


def test_duplicated_identities_expects_unknown_channel_accepted():
    """Test that an unknown channel value is accepted through the StrictStr fallback."""
    model = DuplicatedIdentities(channel="CARRIER_PIGEON")

    assert model.channel == "CARRIER_PIGEON"
