from logging import Logger

from sinch import SinchClient
from sinch.domains.sms.models.v1.shared import MOTextMessage


def handle_sms_event(
    event: MOTextMessage, logger: Logger, sinch_client: SinchClient
):
    """Handle the incoming SMS event by echoing what has been received to the sender."""
    logger.info("Handling event: %s", event.model_dump_json(indent=2))

    sms_request = {
        "to": [event.from_],
        "body": f"You sent: {event.body}",
        "from_": event.to,
    }

    logger.info("Replying with: %s", sms_request)

    response = sinch_client.sms.batches.send_sms(**sms_request)

    logger.info("Response: %s", response)
