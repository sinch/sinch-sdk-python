import pytest
from sinch.domains.conversation.api.v1.utils import (
    build_recipient_dict,
    coerce_recipient,
    split_send_kwargs,
)
from sinch.domains.conversation.models.v1.messages.internal.request import (
    Recipient,
)


class TestBuildRecipientDict:

    @pytest.mark.parametrize(
        "contact_id,recipient_identities,expected",
        [
            ("contact-123", None, {"contact_id": "contact-123"}),
            (
                None,
                [{"channel": "RCS", "identity": "+46701234567"}],
                {"channel_identities": [{"channel": "RCS", "identity": "+46701234567"}]},
            ),
        ],
    )
    def test_build_recipient_dict_expects_valid_input_returns_recipient_dict(
        self, contact_id, recipient_identities, expected
    ):
        """Test that providing contact_id or recipient_identities returns the expected dict."""
        result = build_recipient_dict(
            contact_id=contact_id, recipient_identities=recipient_identities
        )
        assert result == expected

    @pytest.mark.parametrize(
        "contact_id,recipient_identities,error_substring",
        [
            (
                "contact-123",
                [{"channel": "RCS", "identity": "+46701234567"}],
                "Cannot specify both",
            ),
            (None, None, "Must provide either"),
        ],
    )
    def test_build_recipient_dict_expects_value_error_when_invalid(
        self, contact_id, recipient_identities, error_substring
    ):
        """Test that invalid combinations raise ValueError with expected message."""
        with pytest.raises(ValueError) as excinfo:
            build_recipient_dict(
                contact_id=contact_id, recipient_identities=recipient_identities
            )
        assert error_substring in str(excinfo.value)


class TestCoerceRecipient:

    def test_coerce_recipient_expects_recipient_instance_returned_unchanged(self):
        """Passing a Recipient returns the same instance with contact_id preserved."""
        recipient_input = Recipient(contact_id="contact-123")
        result = coerce_recipient(recipient_input)
        assert isinstance(result, Recipient)
        assert result is recipient_input
        assert result.contact_id == "contact-123"

    def test_coerce_recipient_expects_dict_with_contact_id_converted_to_recipient(
        self,
    ):
        """Passing a dict with contact_id returns a new Recipient with that contact_id."""
        recipient_input = {"contact_id": "contact-456"}
        result = coerce_recipient(recipient_input)
        assert isinstance(result, Recipient)
        assert result is not recipient_input
        assert result.contact_id == "contact-456"

    def test_coerce_recipient_expects_dict_with_channel_identities_converted_to_recipient(
        self,
    ):
        """Passing a dict with channel_identities returns Recipient with identified_by."""
        recipient_input = {
            "channel_identities": [{"channel": "RCS", "identity": "+46701234567"}]
        }
        result = coerce_recipient(recipient_input)
        assert isinstance(result, Recipient)
        assert result.identified_by is not None
        assert len(result.identified_by.channel_identities) == 1
        assert (
            result.identified_by.channel_identities[0].identity == "+46701234567"
        )

    def test_coerce_recipient_expects_dict_with_identified_by_converted_to_recipient(
        self,
    ):
        """Passing a dict with identified_by.channel_identities returns Recipient."""
        recipient_input = {
            "identified_by": {
                "channel_identities": [
                    {"channel": "RCS", "identity": "+46701234567"},
                ]
            }
        }
        result = coerce_recipient(recipient_input)
        assert isinstance(result, Recipient)
        assert result.identified_by is not None
        assert len(result.identified_by.channel_identities) == 1
        assert (
            result.identified_by.channel_identities[0].identity == "+46701234567"
        )


class TestSplitSendKwargs:

    @pytest.mark.parametrize(
        "kwargs,expected_message_kwargs,expected_request_kwargs",
        [
            ({}, {}, {}),
            (
                {"text_message": {"text": "Hello"}},
                {"text_message": {"text": "Hello"}},
                {},
            ),
            (
                {"ttl": 10, "callback_url": "https://example.com/callback"},
                {},
                {"ttl": 10, "callback_url": "https://example.com/callback"},
            ),
            (
                {
                    "text_message": {"text": "Hi"},
                    "ttl": 30,
                    "media_message": {"url": "https://example.com/image.jpg"},
                },
                {
                    "text_message": {"text": "Hi"},
                    "media_message": {"url": "https://example.com/image.jpg"},
                },
                {"ttl": 30},
            ),
        ],
    )
    def test_split_send_kwargs_expects_kwargs_split_into_message_and_request(
        self, kwargs, expected_message_kwargs, expected_request_kwargs
    ):
        """Test that kwargs are split into message_kwargs and request_kwargs."""
        message_kwargs, request_kwargs = split_send_kwargs(kwargs)
        assert message_kwargs == expected_message_kwargs
        assert request_kwargs == expected_request_kwargs
