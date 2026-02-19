from sinch.domains.conversation.webhooks.v1.events import (
    ConversationWebhookEventBase,
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageSubmitEvent,
)


def handle_conversation_event(event: ConversationWebhookEventBase, logger):
    """
    Dispatch a Conversation webhook event to the appropriate handler by trigger type.

    :param event: Parsed webhook event (MessageDeliveryReceiptEvent, MessageInboundEvent, etc.).
    :param logger: Logger instance for output.
    """
    if isinstance(event, MessageInboundEvent):
        _handle_message_inbound(event, logger)
    elif isinstance(event, MessageDeliveryReceiptEvent):
        _handle_message_delivery(event, logger)
    elif isinstance(event, MessageSubmitEvent):
        _handle_message_submit(event, logger)
    else:
        logger.info("Conversation webhook: unknown or unhandled trigger %s", getattr(event, "trigger", None))
        logger.debug("Event: %s", event.model_dump_json(indent=2) if hasattr(event, "model_dump_json") else event)


def _handle_message_inbound(event: MessageInboundEvent, logger):
    """Handle MESSAGE_INBOUND: log inbound message."""
    logger.info("## MESSAGE_INBOUND")
    msg = event.message
    contact_msg = msg.contact_message
    channel_identity = msg.channel_identity
    contact_id = msg.contact_id
    channel = channel_identity.channel if channel_identity else "?"
    identity = channel_identity.identity if channel_identity else "?"
    logger.info(
        "A new message has been received on the channel '%s' (identity: %s) from the contact ID '%s'",
        channel,
        identity,
        contact_id,
    )
    if contact_msg:
        if hasattr(contact_msg, "text_message") and contact_msg.text_message:
            logger.info("Text: %s", contact_msg.text_message.text)
        elif hasattr(contact_msg, "media_message") and contact_msg.media_message:
            logger.info("Media: %s", getattr(contact_msg.media_message, "url", contact_msg.media_message))
        elif hasattr(contact_msg, "fallback_message") and contact_msg.fallback_message:
            logger.info("Fallback: %s", contact_msg.fallback_message)
        else:
            logger.info("Contact message: %s", contact_msg)


def _handle_message_delivery(event: MessageDeliveryReceiptEvent, logger):
    """Handle MESSAGE_DELIVERY: log delivery status and failure reason if failed."""
    logger.info("## MESSAGE_DELIVERY")
    report = event.message_delivery_report
    status = report.status
    logger.info("Message delivery status: '%s'", status)
    if status == "FAILED" and report.reason:
        logger.info(
            "Reason: %s (%s) - %s",
            report.reason.code,
            getattr(report.reason, "sub_code", ""),
            report.reason.description,
        )


def _handle_message_submit(event: MessageSubmitEvent, logger):
    """Handle MESSAGE_SUBMIT: log that the message was submitted to the channel."""
    logger.info("## MESSAGE_SUBMIT")
    submit_notification = event.message_submit_notification
    channel_identity = submit_notification.channel_identity
    channel = channel_identity.channel if channel_identity else "?"
    identity = channel_identity.identity if channel_identity else "?"
    logger.info(
        "The following message has been submitted on the channel '%s' (identity: %s) to the contact ID '%s'",
        channel,
        identity,
        submit_notification.contact_id,
    )
    if submit_notification.submitted_message:
        logger.debug("Submitted message: %s", submit_notification.submitted_message)
