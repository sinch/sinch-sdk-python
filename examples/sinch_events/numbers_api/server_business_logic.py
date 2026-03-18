from sinch.domains.numbers.sinch_events.v1.events import NumberSinchEvent


def handle_numbers_event(numbers_event: NumberSinchEvent, logger):
    """
    This method handles a Numbers event.
    Args:
        numbers_event (NumberSinchEvent): The Numbers event data.
        logger (logging.Logger, optional): Logger instance for logging. Defaults to None.
    """
    logger.info(f'Handling Numbers event:\n{numbers_event.model_dump_json(indent=2)}')
