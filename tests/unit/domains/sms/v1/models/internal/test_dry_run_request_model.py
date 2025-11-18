import pytest
from pydantic import ValidationError
from datetime import datetime, timezone
from sinch.domains.sms.models.v1.internal.dry_run_request import (
    DryRunTextRequest,
    DryRunBinaryRequest,
    DryRunMediaRequest,
    DryRunRequest,
)
from sinch.domains.sms.models.v1.shared import MediaBody


@pytest.fixture
def sample_text_request_data():
    return {
        "to": ["+12017777777", "+12018888888"],
        "from_": "+12015555555",
        "body": "Hello World!",
    }


@pytest.fixture
def sample_binary_request_data():
    return {
        "to": ["+12017777777"],
        "from_": "+12015555555",
        "body": "SGVsbG8gV29ybGQh",
        "udh": "06050423F423F4",
    }


@pytest.fixture
def sample_media_request_data():
    return {
        "to": ["+12017777777"],
        "from_": "+12015555555",
        "body": MediaBody(
            url="https://capybara.com/image.jpg",
            message="Check out this image!",
            subject="Image",
        ),
    }


class TestDryRunMixin:
    """Tests for DryRunMixin fields (per_recipient and number_of_recipients)."""

    def test_dry_run_mixin_expects_per_recipient_defaults_and_values(
        self, sample_text_request_data
    ):
        """Test per_recipient defaults to False and can be set to True/False."""
        # Default value
        request = DryRunTextRequest(**sample_text_request_data)
        assert request.per_recipient is None

        request = DryRunTextRequest(
            **sample_text_request_data, per_recipient=True
        )
        assert request.per_recipient is True

        request = DryRunTextRequest(
            **sample_text_request_data, per_recipient=False
        )
        assert request.per_recipient is False

    def test_dry_run_mixin_expects_number_of_recipients_defaults_to_none(
        self, sample_text_request_data
    ):
        """Test that number_of_recipients defaults to None."""
        request = DryRunTextRequest(**sample_text_request_data)
        assert request.number_of_recipients is None

    @pytest.mark.parametrize(
        "number_of_recipients",
        [0, 100, 1000],
    )
    def test_dry_run_mixin_expects_valid_number_of_recipients(
        self, sample_text_request_data, number_of_recipients
    ):
        """Test that number_of_recipients accepts valid values (0-1000)."""
        request = DryRunTextRequest(
            **sample_text_request_data,
            number_of_recipients=number_of_recipients,
        )
        assert request.number_of_recipients == number_of_recipients


    def test_dry_run_mixin_expects_number_of_recipients_not_string(
        self, sample_text_request_data
    ):
        """Test that number_of_recipients must be an integer."""
        with pytest.raises(ValidationError):
            DryRunTextRequest(
                **sample_text_request_data, number_of_recipients="100"
            )


class TestDryRunTextRequest:
    """Tests for DryRunTextRequest model."""

    def test_dry_run_text_request_expects_valid_inputs_and_all_fields(
        self, sample_text_request_data
    ):
        """Test DryRunTextRequest with valid inputs and all optional fields."""
        request = DryRunTextRequest(**sample_text_request_data)
        assert request.to == sample_text_request_data["to"]
        assert request.from_ == sample_text_request_data["from_"]
        assert request.body == sample_text_request_data["body"]
        assert request.type == "mt_text"
        assert request.per_recipient is None
        assert request.number_of_recipients is None

        send_at = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        expire_at = datetime(2025, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

        request = DryRunTextRequest(
            **sample_text_request_data,
            per_recipient=True,
            number_of_recipients=50,
            delivery_report="summary",
            send_at=send_at,
            expire_at=expire_at,
            callback_url="https://capybara.com/callback",
            client_reference="test-ref",
            feedback_enabled=True,
            flash_message=False,
            max_number_of_message_parts=3,
            truncate_concat=True,
            from_ton=1,
            from_npi=1,
        )

        assert request.per_recipient is True
        assert request.number_of_recipients == 50
        assert request.delivery_report == "summary"
        assert request.send_at == send_at
        assert request.expire_at == expire_at
        assert request.callback_url == "https://capybara.com/callback"
        assert request.client_reference == "test-ref"
        assert request.feedback_enabled is True
        assert request.flash_message is False
        assert request.max_number_of_message_parts == 3
        assert request.truncate_concat is True
        assert request.from_ton == 1
        assert request.from_npi == 1

    def test_dry_run_text_request_expects_required_fields_and_inheritance(
        self, sample_text_request_data
    ):
        """Test required fields validation and inheritance from TextRequest."""
        with pytest.raises(ValidationError) as exc_info:
            DryRunTextRequest()
        assert "to" in str(exc_info.value) or "body" in str(exc_info.value)

        request = DryRunTextRequest(**sample_text_request_data)
        # Verify TextRequest fields
        assert hasattr(request, "to")
        assert hasattr(request, "from_")
        assert hasattr(request, "body")
        assert hasattr(request, "type")
        assert hasattr(request, "delivery_report")
        assert hasattr(request, "send_at")
        assert hasattr(request, "expire_at")
        # Verify DryRunMixin fields
        assert hasattr(request, "per_recipient")
        assert hasattr(request, "number_of_recipients")


class TestDryRunBinaryRequest:
    """Tests for DryRunBinaryRequest model."""

    def test_dry_run_binary_request_expects_valid_inputs_and_all_fields(
        self, sample_binary_request_data
    ):
        """Test DryRunBinaryRequest with valid inputs and all optional fields."""
        request = DryRunBinaryRequest(**sample_binary_request_data)
        assert request.to == sample_binary_request_data["to"]
        assert request.from_ == sample_binary_request_data["from_"]
        assert request.body == sample_binary_request_data["body"]
        assert request.udh == sample_binary_request_data["udh"]
        assert request.type == "mt_binary"
        assert request.per_recipient is None
        assert request.number_of_recipients is None

        send_at = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        expire_at = datetime(2025, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

        request = DryRunBinaryRequest(
            **sample_binary_request_data,
            per_recipient=True,
            number_of_recipients=25,
            delivery_report="full",
            send_at=send_at,
            expire_at=expire_at,
            callback_url="https://capybara.com/callback",
            client_reference="binary-ref",
            feedback_enabled=False,
            from_ton=0,
            from_npi=1,
        )

        assert request.per_recipient is True
        assert request.number_of_recipients == 25
        assert request.delivery_report == "full"
        assert request.send_at == send_at
        assert request.expire_at == expire_at
        assert request.callback_url == "https://capybara.com/callback"
        assert request.client_reference == "binary-ref"
        assert request.feedback_enabled is False
        assert request.from_ton == 0
        assert request.from_npi == 1

    def test_dry_run_binary_request_expects_required_fields_and_inheritance(
        self, sample_binary_request_data
    ):
        """Test required fields validation and inheritance from BinaryRequest."""
        with pytest.raises(ValidationError) as exc_info:
            DryRunBinaryRequest()
        error_str = str(exc_info.value)
        assert "to" in error_str or "body" in error_str or "udh" in error_str

        request = DryRunBinaryRequest(**sample_binary_request_data)
        assert hasattr(request, "to")
        assert hasattr(request, "from_")
        assert hasattr(request, "body")
        assert hasattr(request, "udh")
        assert hasattr(request, "type")
        assert hasattr(request, "delivery_report")

        assert hasattr(request, "per_recipient")
        assert hasattr(request, "number_of_recipients")


class TestDryRunMediaRequest:
    """Tests for DryRunMediaRequest model."""

    def test_dry_run_media_request_expects_valid_inputs_and_all_fields(
        self, sample_media_request_data
    ):
        """Test DryRunMediaRequest with valid inputs and all optional fields."""
        request = DryRunMediaRequest(**sample_media_request_data)
        assert request.to == sample_media_request_data["to"]
        assert request.from_ == sample_media_request_data["from_"]
        assert isinstance(request.body, MediaBody)
        assert request.body.url == sample_media_request_data["body"].url
        assert request.type == "mt_media"
        assert request.per_recipient is None
        assert request.number_of_recipients is None

        send_at = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        expire_at = datetime(2025, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

        request = DryRunMediaRequest(
            **sample_media_request_data,
            per_recipient=True,
            number_of_recipients=75,
            delivery_report="summary",
            send_at=send_at,
            expire_at=expire_at,
            callback_url="https://capybara.com/callback",
            client_reference="media-ref",
            feedback_enabled=True,
        )

        assert request.per_recipient is True
        assert request.number_of_recipients == 75
        assert request.delivery_report == "summary"
        assert request.send_at == send_at
        assert request.expire_at == expire_at
        assert request.callback_url == "https://capybara.com/callback"
        assert request.client_reference == "media-ref"
        assert request.feedback_enabled is True

    def test_dry_run_media_request_expects_required_fields_and_inheritance(
        self, sample_media_request_data
    ):
        """Test required fields validation and inheritance from MediaRequest."""
        with pytest.raises(ValidationError) as exc_info:
            DryRunMediaRequest()
        assert "to" in str(exc_info.value) or "body" in str(exc_info.value)

        request = DryRunMediaRequest(**sample_media_request_data)
        assert hasattr(request, "to")
        assert hasattr(request, "from_")
        assert hasattr(request, "body")
        assert hasattr(request, "type")
        assert hasattr(request, "delivery_report")

        assert hasattr(request, "per_recipient")
        assert hasattr(request, "number_of_recipients")


class TestDryRunRequestUnion:
    """Tests for DryRunRequest Union type."""

    def test_dry_run_request_union_expects_accepts_text_request_object(
        self, sample_text_request_data
    ):
        """Test that DryRunRequest Union accepts DryRunTextRequest object."""
        from pydantic import TypeAdapter

        text_request = DryRunTextRequest(**sample_text_request_data)
        adapter = TypeAdapter(DryRunRequest)
        validated = adapter.validate_python(text_request.model_dump())
        assert isinstance(validated, DryRunTextRequest)

    def test_dry_run_request_union_expects_accepts_binary_request_object(
        self, sample_binary_request_data
    ):
        """Test that DryRunRequest Union accepts DryRunBinaryRequest object."""
        from pydantic import TypeAdapter

        binary_request = DryRunBinaryRequest(**sample_binary_request_data)
        adapter = TypeAdapter(DryRunRequest)
        validated = adapter.validate_python(binary_request.model_dump())
        assert isinstance(validated, DryRunBinaryRequest)

    def test_dry_run_request_union_expects_accepts_media_request_object(
        self, sample_media_request_data
    ):
        """Test that DryRunRequest Union accepts DryRunMediaRequest object."""
        from pydantic import TypeAdapter

        media_request = DryRunMediaRequest(**sample_media_request_data)
        adapter = TypeAdapter(DryRunRequest)
        validated = adapter.validate_python(media_request.model_dump())
        assert isinstance(validated, DryRunMediaRequest)

    def test_dry_run_request_union_expects_accepts_dict_inputs(
        self,
        sample_text_request_data,
        sample_binary_request_data,
        sample_media_request_data,
    ):
        """Test that DryRunRequest Union accepts dict input for all types."""
        from pydantic import TypeAdapter

        adapter = TypeAdapter(DryRunRequest)

        validated = adapter.validate_python(sample_text_request_data)
        assert isinstance(validated, DryRunTextRequest)

        validated = adapter.validate_python(sample_binary_request_data)
        assert isinstance(validated, DryRunBinaryRequest)

        media_data = sample_media_request_data.copy()
        media_data["body"] = media_data["body"].model_dump()
        validated = adapter.validate_python(media_data)
        assert isinstance(validated, DryRunMediaRequest)

    def test_dry_run_request_union_expects_rejects_invalid_dict(self):
        """Test that DryRunRequest Union rejects invalid dict."""
        from pydantic import TypeAdapter, ValidationError

        adapter = TypeAdapter(DryRunRequest)
        with pytest.raises(ValidationError):
            adapter.validate_python({"invalid": "data"})
