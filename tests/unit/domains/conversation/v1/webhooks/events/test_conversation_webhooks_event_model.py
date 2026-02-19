"""Unit tests for Conversation webhook event models."""
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.webhooks.v1.events import (
    ConversationWebhookEventBase,
    MessageDeliveryReceiptEvent,
    MessageDeliveryReport,
    MessageInboundEvent,
    MessageSubmitEvent,
    MessageSubmitNotification,
)


@pytest.fixture
def message_delivery_report_data():
    return {
        "message_id": "01EQBC1A3BEK731GY4YXEN0C2R",
        "conversation_id": "01EPYATA64TMNZ1FV02JKF12JF",
        "status": "QUEUED_ON_CHANNEL",
        "contact_id": "01EXA07N79THJ20WSN6AS30TMW",
        "channel_identity": {"channel": "WHATSAPP", "identity": "1234567890"},
    }


def test_message_delivery_report_expects_parsed(message_delivery_report_data):
    report = MessageDeliveryReport(**message_delivery_report_data)
    assert report.message_id == "01EQBC1A3BEK731GY4YXEN0C2R"
    assert report.conversation_id == "01EPYATA64TMNZ1FV02JKF12JF"
    assert report.status == "QUEUED_ON_CHANNEL"
    assert report.contact_id == "01EXA07N79THJ20WSN6AS30TMW"
    assert report.channel_identity is not None
    assert report.channel_identity.channel == "WHATSAPP"
    assert report.channel_identity.identity == "1234567890"


def test_message_delivery_receipt_event_expects_parsed(message_delivery_report_data):
    payload = {
        "trigger": "MESSAGE_DELIVERY",
        "app_id": "app1",
        "project_id": "proj1",
        "accepted_time": "2020-11-17T15:09:11.659Z",
        "message_delivery_report": message_delivery_report_data,
    }
    event = MessageDeliveryReceiptEvent(**payload)
    assert event.trigger == "MESSAGE_DELIVERY"
    assert event.app_id == "app1"
    assert event.message_delivery_report is not None
    assert event.message_delivery_report.message_id == "01EQBC1A3BEK731GY4YXEN0C2R"


def test_message_inbound_event_expects_parsed():
    payload = {
        "trigger": "MESSAGE_INBOUND",
        "app_id": "app1",
        "message": {
            "contact_id": "contact1",
            "contact_message": {"text_message": {"text": "Hello"}},
            "channel_identity": {"channel": "SMS", "identity": "+15551234567"},
        },
    }
    event = MessageInboundEvent(**payload)
    assert event.trigger == "MESSAGE_INBOUND"
    assert event.message is not None
    assert event.message.contact_id == "contact1"
    assert event.message.contact_message.text_message.text == "Hello"


def test_message_submit_event_expects_parsed():
    payload = {
        "trigger": "MESSAGE_SUBMIT",
        "app_id": "app1",
        "message_submit_notification": {
            "contact_id": "contact1",
            "channel_identity": {"channel": "MESSENGER", "identity": "123"},
        },
    }
    event = MessageSubmitEvent(**payload)
    assert event.trigger == "MESSAGE_SUBMIT"
    assert event.message_submit_notification is not None
    assert event.message_submit_notification.contact_id == "contact1"


def test_conversation_webhook_event_base_optional_fields():
    payload = {"trigger": "UNKNOWN", "app_id": "app1"}
    event = ConversationWebhookEventBase(**payload)
    assert event.trigger == "UNKNOWN"
    assert event.app_id == "app1"
    assert event.project_id is None
    assert event.accepted_time is None
    assert event.event_time is None


def test_message_delivery_receipt_event_wrong_trigger_expects_validation_error(message_delivery_report_data):
    payload = {
        "trigger": "MESSAGE_INBOUND",
        "message_delivery_report": message_delivery_report_data,
    }
    with pytest.raises(ValidationError):
        MessageDeliveryReceiptEvent(**payload)
