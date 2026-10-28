from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.conversations.internal.inject_message_request import (
    InjectMessageRequest,
)
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    TextAppMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    ChoiceResponseContactMessage,
    TextContactMessage,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)

ACCEPT_TIME = datetime(2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc)
CHANNEL_IDENTITY = {
    "channel": "MESSENGER",
    "identity": "7968425018576406",
    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
}


def test_inject_message_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = InjectMessageRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        app_message={"text_message": {"text": "Hello"}},
        accept_time=ACCEPT_TIME,
        channel_identity=CHANNEL_IDENTITY,
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        direction="TO_CONTACT",
        sender_id="sender-1",
        processing_mode="CONVERSATION",
        metadata="my metadata",
    )

    assert model.conversation_id == "01W4FFL35P4NC4K35CONVERS001"
    assert isinstance(model.app_message, TextAppMessage)
    assert model.app_message.text_message.text == "Hello"
    assert model.accept_time == ACCEPT_TIME
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.channel == "MESSENGER"
    assert model.channel_identity.identity == "7968425018576406"
    assert model.channel_identity.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert model.direction == "TO_CONTACT"
    assert model.sender_id == "sender-1"
    assert model.processing_mode == "CONVERSATION"
    assert model.metadata == "my metadata"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump == {
        "conversation_id": "01W4FFL35P4NC4K35CONVERS001",
        "app_message": {"text_message": {"text": "Hello"}},
        "accept_time": "2026-10-09T10:00:00Z",
        "channel_identity": CHANNEL_IDENTITY,
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "direction": "TO_CONTACT",
        "sender_id": "sender-1",
        "processing_mode": "CONVERSATION",
        "metadata": "my metadata",
    }


def test_inject_message_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = InjectMessageRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        accept_time=ACCEPT_TIME,
        channel_identity=CHANNEL_IDENTITY,
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        direction="TO_CONTACT",
    )

    assert model.app_message is None
    assert model.contact_message is None
    assert model.sender_id is None
    assert model.processing_mode is None
    assert model.metadata is None


def test_inject_message_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        InjectMessageRequest(
            conversation_id="01W4FFL35P4NC4K35CONVERS001",
            accept_time=ACCEPT_TIME,
            channel_identity=CHANNEL_IDENTITY,
            direction="TO_CONTACT",
        )


def test_inject_message_request_expects_text_contact_message_variant_accepted():
    """Test that a text contact message is resolved to TextContactMessage."""
    model = InjectMessageRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        contact_message={"text_message": {"text": "Hi"}},
        accept_time=ACCEPT_TIME,
        channel_identity=CHANNEL_IDENTITY,
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        direction="TO_APP",
    )

    assert isinstance(model.contact_message, TextContactMessage)
    assert model.contact_message.text_message.text == "Hi"


def test_inject_message_request_expects_choice_response_contact_message_variant_accepted():
    """Test that a choice response contact message is resolved to its variant."""
    model = InjectMessageRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        contact_message={
            "choice_response_message": {
                "message_id": "01W4FFL35P4NC4K35MESSAGE001",
                "postback_data": "postback",
            }
        },
        accept_time=ACCEPT_TIME,
        channel_identity=CHANNEL_IDENTITY,
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        direction="TO_APP",
    )

    assert isinstance(model.contact_message, ChoiceResponseContactMessage)
    assert (
        model.contact_message.choice_response_message.postback_data
        == "postback"
    )


@pytest.mark.parametrize("field", ["app_message", "contact_message"])
def test_inject_message_request_expects_explicit_none_message_rejected(field):
    """Test that app_message and contact_message can be omitted but not set to None."""
    with pytest.raises(ValidationError):
        InjectMessageRequest(
            conversation_id="01W4FFL35P4NC4K35CONVERS001",
            accept_time=ACCEPT_TIME,
            channel_identity=CHANNEL_IDENTITY,
            contact_id="01W4FFL35P4NC4K35CONTACT001",
            direction="TO_APP",
            **{field: None},
        )
