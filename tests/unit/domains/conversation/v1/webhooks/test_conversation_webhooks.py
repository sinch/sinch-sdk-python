"""Unit tests for Conversation API webhooks (signature validation and parse_event)."""
from datetime import datetime, timezone

import pytest

from sinch.domains.authentication.webhooks.v1.authentication_validation import (
    compute_signed_data,
    calculate_webhook_signature,
)
from sinch.domains.conversation.webhooks.v1 import ConversationWebhooks
from sinch.domains.conversation.webhooks.v1.events import (
    ConversationWebhookEventBase,
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageSubmitEvent,
)


@pytest.fixture
def webhook_secret():
    return "foo_secret1234"


@pytest.fixture
def conversation_webhooks(webhook_secret):
    return ConversationWebhooks(webhook_secret)


@pytest.fixture
def sample_body():
    return (
        '{"app_id":"01EB37HMH1M6SV18BSNS3G135H","accepted_time":"2020-11-17T15:09:11.659Z",'
        '"project_id":"c36f3d3d-1513-2edd-ae42-11995557ff61","trigger":"MESSAGE_DELIVERY",'
        '"message_delivery_report":{"message_id":"01EQBC1A3BEK731GY4YXEN0C2R",'
        '"conversation_id":"01EPYATA64TMNZ1FV02JKF12JF","status":"QUEUED_ON_CHANNEL",'
        '"contact_id":"01EXA07N79THJ20WSN6AS30TMW"}}'
    )


def _make_signed_headers(body: str, secret: str, nonce: str = "01FJA8B4A7BM43YGWSG9GBV067", timestamp: str = "1634579353"):
    signed_data = compute_signed_data(body, nonce, timestamp)
    sig = calculate_webhook_signature(signed_data, secret)
    return {
        "x-sinch-webhook-signature": sig,
        "x-sinch-webhook-signature-nonce": nonce,
        "x-sinch-webhook-signature-timestamp": timestamp,
    }


def test_validate_signature_valid_expects_true(conversation_webhooks, sample_body, webhook_secret):
    headers = _make_signed_headers(sample_body, webhook_secret)
    assert conversation_webhooks.validate_signature(sample_body, headers) is True


def test_validate_signature_missing_headers_expects_false(conversation_webhooks, sample_body):
    assert conversation_webhooks.validate_signature(sample_body, {}) is False


def test_validate_signature_invalid_signature_expects_false(conversation_webhooks, sample_body):
    headers = {
        "x-sinch-webhook-signature": "invalid",
        "x-sinch-webhook-signature-nonce": "01FJA8B4A7BM43YGWSG9GBV067",
        "x-sinch-webhook-signature-timestamp": "1634579353",
    }
    assert conversation_webhooks.validate_signature(sample_body, headers) is False


def test_parse_event_message_delivery_expects_message_delivery_receipt_event(conversation_webhooks):
    payload = {
        "trigger": "MESSAGE_DELIVERY",
        "app_id": "01EB37HMH1M6SV18BSNS3G135H",
        "project_id": "c36f3d3d-1513-2edd-ae42-11995557ff61",
        "accepted_time": "2020-11-17T15:09:11.659Z",
        "event_time": "2020-11-17T15:09:13.267185Z",
        "message_delivery_report": {
            "message_id": "01EQBC1A3BEK731GY4YXEN0C2R",
            "conversation_id": "01EPYATA64TMNZ1FV02JKF12JF",
            "status": "QUEUED_ON_CHANNEL",
            "contact_id": "01EXA07N79THJ20WSN6AS30TMW",
        },
    }
    event = conversation_webhooks.parse_event(payload)
    assert isinstance(event, MessageDeliveryReceiptEvent)
    assert event.trigger == "MESSAGE_DELIVERY"
    assert event.message_delivery_report is not None
    assert event.message_delivery_report.message_id == "01EQBC1A3BEK731GY4YXEN0C2R"
    assert event.message_delivery_report.status == "QUEUED_ON_CHANNEL"
    assert event.accepted_time == datetime(2020, 11, 17, 15, 9, 11, 659000, tzinfo=timezone.utc)


def test_parse_event_message_inbound_expects_message_inbound_event(conversation_webhooks):
    payload = {
        "trigger": "MESSAGE_INBOUND",
        "app_id": "01EB37HMH1M6SV18BSNS3G135H",
        "project_id": "c36f3d3d-1513-2edd-ae42-11995557ff61",
        "accepted_time": "2020-11-17T15:09:11.659Z",
        "message": {
            "contact_id": "01EXA07N79THJ20WSN6AS30TMW",
            "contact_message": {"text_message": {"text": "Hello"}},
            "channel_identity": {"channel": "WHATSAPP", "identity": "1234567890"},
        },
    }
    event = conversation_webhooks.parse_event(payload)
    assert isinstance(event, MessageInboundEvent)
    assert event.trigger == "MESSAGE_INBOUND"
    assert event.message is not None
    assert event.message.contact_id == "01EXA07N79THJ20WSN6AS30TMW"
    assert event.message.contact_message is not None
    assert hasattr(event.message.contact_message, "text_message")
    assert event.message.contact_message.text_message.text == "Hello"


def test_parse_event_message_submit_expects_message_submit_event(conversation_webhooks):
    payload = {
        "trigger": "MESSAGE_SUBMIT",
        "app_id": "01EB37HMH1M6SV18BSNS3G135H",
        "project_id": "c36f3d3d-1513-2edd-ae42-11995557ff61",
        "accepted_time": "2020-11-17T15:09:11.659Z",
        "message_submit_notification": {
            "contact_id": "01EXA07N79THJ20WSN6AS30TMW",
            "channel_identity": {"channel": "WHATSAPP", "identity": "1234567890"},
            "submitted_message": {"text_message": {"text": "Hi"}},
        },
    }
    event = conversation_webhooks.parse_event(payload)
    assert isinstance(event, MessageSubmitEvent)
    assert event.trigger == "MESSAGE_SUBMIT"
    assert event.message_submit_notification is not None
    assert event.message_submit_notification.contact_id == "01EXA07N79THJ20WSN6AS30TMW"


def test_parse_event_unknown_trigger_expects_base_event(conversation_webhooks):
    payload = {
        "trigger": "CONTACT_CREATE",
        "app_id": "01EB37HMH1M6SV18BSNS3G135H",
        "project_id": "c36f3d3d-1513-2edd-ae42-11995557ff61",
    }
    event = conversation_webhooks.parse_event(payload)
    assert isinstance(event, ConversationWebhookEventBase)
    assert event.trigger == "CONTACT_CREATE"
    assert not isinstance(event, (MessageDeliveryReceiptEvent, MessageInboundEvent, MessageSubmitEvent))


def test_parse_event_json_string_expects_parsed(conversation_webhooks):
    payload_str = '{"trigger":"MESSAGE_DELIVERY","app_id":"app1","message_delivery_report":{"status":"SUCCESS"}}'
    event = conversation_webhooks.parse_event(payload_str)
    assert isinstance(event, MessageDeliveryReceiptEvent)
    assert event.app_id == "app1"
    assert event.message_delivery_report.status == "SUCCESS"


def test_parse_event_invalid_json_expects_value_error(conversation_webhooks):
    with pytest.raises(ValueError, match="Failed to decode JSON"):
        conversation_webhooks.parse_event("not json")


def test_parse_event_without_trigger_uses_discriminant(conversation_webhooks):
    """Payloads without 'trigger' are parsed by which key is present (OpenAPI oneOf)."""
    payload = {
        "app_id": "app1",
        "project_id": "proj1",
        "accepted_time": "2020-11-17T15:09:11.659Z",
        "message_delivery_report": {
            "message_id": "msg1",
            "status": "DELIVERED",
        },
    }
    event = conversation_webhooks.parse_event(payload)
    assert isinstance(event, MessageDeliveryReceiptEvent)
    assert event.trigger == "MESSAGE_DELIVERY"
    assert event.message_delivery_report.message_id == "msg1"
