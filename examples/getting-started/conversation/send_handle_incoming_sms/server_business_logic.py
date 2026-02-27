"""
On inbound SMS (MO), send a reply (MT) to the same number: "Your message said: <text>".
Uses channel identity (SMS + phone number) only; app is in DISPATCH mode.
"""

from sinch.domains.conversation.models.v1.webhooks import MessageInboundEvent


def handle_conversation_event(event, logger, sinch_client, app_id):
    """Webhook entry: handle only MESSAGE_INBOUND; delegate to inbound handler."""
    if not isinstance(event, MessageInboundEvent):
        return
    _handle_message_inbound(event, logger, sinch_client, app_id)


def _get_mo_text(event: MessageInboundEvent) -> str:
    """Return the inbound message text, or a short placeholder if none."""
    msg = event.message
    contact_msg = msg.contact_message
    if getattr(contact_msg, "text_message", None):
        return contact_msg.text_message.text or "(empty)"
    return "(no text content)"


def _handle_message_inbound(event: MessageInboundEvent, logger, sinch_client, app_id):
    """Parse MO, then send MT echo to the same number via Conversation API."""
    msg = event.message
    channel_identity = msg.channel_identity
    if not channel_identity:
        logger.warning("MESSAGE_INBOUND with no channel_identity")
        return

    identity = channel_identity.identity
    mo_text = _get_mo_text(event)
    logger.info("MO SMS from %s: %s", identity, mo_text)

    if not app_id:
        logger.warning("CONVERSATION_APP_ID not set; skipping MT reply.")
        return

    reply_text = f"Your message said: {mo_text}"
    response = sinch_client.conversation.messages.send_text_message(
        app_id=app_id,
        text=reply_text,
        recipient_identities=[{"channel": "SMS", "identity": identity}],
    )
    logger.info("MT reply sent to %s (channel identity): %s", identity, reply_text[:60])
    logger.debug(
        "Response: message_id=%s accepted_time=%s",
        response.message_id,
        response.accepted_time
    )
