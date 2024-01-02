from sinch.domains.numbers.models.callbacks.responses import UpdateNumbersCallbackConfigurationResponse


def test_update_callback_configuration_configuration(sinch_client_sync):
    update_callback_configuration_response = sinch_client_sync.numbers.callbacks.update_configuration(
        hmac_secret="Secret"
    )
    assert isinstance(update_callback_configuration_response, UpdateNumbersCallbackConfigurationResponse)
