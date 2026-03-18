from sinch.domains.sms.sinch_events.v1.events.sms_sinch_event import IncomingSMSWebhookEvent


def handle_sms_event(sms_event: IncomingSMSWebhookEvent, logger):
    """
    This method handles an SMS event.
    Args:
        sms_event (IncomingSMSWebhookEvent): The SMS event data.
        logger (logging.Logger, optional): Logger instance for logging. Defaults to None.
    """
    logger.info(f'Handling SMS event:\n{sms_event.model_dump_json(indent=2)}')
