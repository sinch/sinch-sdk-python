"""Unit tests for Conversation API webhooks (signature validation and parse_event)."""
from datetime import datetime, timezone

import pytest

from sinch.domains.conversation.webhooks.v1 import ConversationWebhooks
from sinch.domains.conversation.models.v1.webhooks import (
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
        '"project_id":"c36f3d3d-1513-2edd-ae42-11995557ff61",'
        '"message_delivery_report":{"message_id":"01EQBC1A3BEK731GY4YXEN0C2R",'
        '"conversation_id":"01EPYATA64TMNZ1FV02JKF12JF","status":"QUEUED_ON_CHANNEL",'
        '"contact_id":"01EXA07N79THJ20WSN6AS30TMW"}}'
    )


VALID_SIGNATURE_HEADERS = {
    "x-sinch-webhook-signature": "Yc+3R1pIS78xLASybulhs8BsSo9BPB3Pr92QCUoczfk=",
    "x-sinch-webhook-signature-nonce": "01FJA8B4A7BM43YGWSG9GBV067",
    "x-sinch-webhook-signature-timestamp": "1634579353",
}


def test_validate_authentication_header_valid_expects_true(conversation_webhooks, sample_body):
    assert conversation_webhooks.validate_authentication_header(
        VALID_SIGNATURE_HEADERS, sample_body
    ) is True


def test_validate_authentication_header_missing_headers_expects_false(conversation_webhooks, sample_body):
    assert conversation_webhooks.validate_authentication_header({}, sample_body) is False


def test_validate_authentication_header_invalid_signature_expects_false(conversation_webhooks, sample_body):
    headers = {
        "x-sinch-webhook-signature": "invalid",
        "x-sinch-webhook-signature-nonce": "01FJA8B4A7BM43YGWSG9GBV067",
        "x-sinch-webhook-signature-timestamp": "1634579353",
    }
    assert conversation_webhooks.validate_authentication_header(headers, sample_body) is False


def test_parse_event_message_delivery_expects_message_delivery_receipt_event(conversation_webhooks):
    payload = {
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
    assert event.message_delivery_report is not None
    assert event.message_delivery_report.message_id == "01EQBC1A3BEK731GY4YXEN0C2R"
    assert event.message_delivery_report.status == "QUEUED_ON_CHANNEL"
    assert event.accepted_time == datetime(2020, 11, 17, 15, 9, 11, 659000, tzinfo=timezone.utc)


def test_parse_event_message_inbound_expects_message_inbound_event(conversation_webhooks):
    payload = {
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
    assert event.message is not None
    assert event.message.contact_id == "01EXA07N79THJ20WSN6AS30TMW"
    assert event.message.contact_message is not None
    assert hasattr(event.message.contact_message, "text_message")
    assert event.message.contact_message.text_message.text == "Hello"


def test_parse_event_message_submit_expects_message_submit_event(conversation_webhooks):
    payload = {
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
    assert event.message_submit_notification is not None
    assert event.message_submit_notification.contact_id == "01EXA07N79THJ20WSN6AS30TMW"


def test_parse_event_json_string_expects_parsed(conversation_webhooks):
    payload_str = '{"app_id":"app1","message_delivery_report":{"status":"DELIVERED"}}'
    event = conversation_webhooks.parse_event(payload_str)
    assert isinstance(event, MessageDeliveryReceiptEvent)
    assert event.app_id == "app1"
    assert event.message_delivery_report.status == "DELIVERED"


def test_parse_event_invalid_json_expects_value_error(conversation_webhooks):
    with pytest.raises(ValueError, match="Failed to decode JSON"):
        conversation_webhooks.parse_event("not json")
