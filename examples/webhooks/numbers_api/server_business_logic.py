from sinch.domains.numbers.webhooks.v1.events.numbers_webhooks_event import NumbersWebhooksEvent


def handle_numbers_event(numbers_event: NumbersWebhooksEvent, logger):
    """
    This method handles a Numbers event.
    Args:
        numbers_event (NumbersWebhooksEvent): The Numbers event data.
        logger (logging.Logger, optional): Logger instance for logging. Defaults to None.
    """
    logger.info(f'Handling Numbers event:\n{numbers_event.model_dump_json(indent=2)}')
