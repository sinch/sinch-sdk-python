from sinch.domains.sms.webhooks.v1.events.sms_webhooks_event import IncomingSMSWebhookEvent


def handle_sms_event(sms_event: IncomingSMSWebhookEvent, logger):
    """
    This method handles an SMS event.
    Args:
        sms_event (SmsWebhooksEvent): The SMS event data.
        logger (logging.Logger, optional): Logger instance for logging. Defaults to None.
    """
    logger.info(f'Handling SMS event:\n{sms_event.model_dump_json(indent=2)}')
