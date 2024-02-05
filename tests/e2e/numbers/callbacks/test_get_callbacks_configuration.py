from sinch.domains.numbers.models.callbacks.responses import GetNumbersCallbackConfigurationResponse


def test_get_callback_configuration_configuration(sinch_client_sync):
    get_callback_configuration_response = sinch_client_sync.numbers.callbacks.get_configuration()
    assert isinstance(get_callback_configuration_response, GetNumbersCallbackConfigurationResponse)
