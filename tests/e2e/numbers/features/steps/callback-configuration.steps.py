from behave import given, when, then

from sinch.domains.numbers.api.v1.exceptions import NumberNotFoundException
from sinch.domains.numbers.models.v1.errors import NotFoundError


@given('the Numbers service "Callback Configuration" is available')
def step_callback_config_service_is_available(context):
    """Ensures the Sinch client is initialized"""
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'


@when('I send a request to retrieve the callback configuration')
def step_retrieve_callback_configuration(context):
    context.response = context.sinch.numbers.callback_configuration.get()


@then('the response contains the project\'s callback configuration')
def step_check_callback_configuration(context):
    assert context.response.project_id == '12c0ffee-dada-beef-cafe-baadc0de5678'
    assert context.response.hmac_secret == '0default-pass-word-*max-36characters'


@when('I send a request to update the callback configuration with the secret "{hmac_secret}"')
def step_update_callback_configuration(context, hmac_secret):
    try:
        context.response = context.sinch.numbers.callback_configuration.update(hmac_secret=hmac_secret)
        context.error = None
    except NumberNotFoundException as e:
        context.error = e


@then('the response contains the updated project\'s callback configuration')
def step_check_updated_callback_configuration(context):
    assert context.response.project_id == '12c0ffee-dada-beef-cafe-baadc0de5678'
    assert context.response.hmac_secret == 'strongPa$$PhraseWith36CharactersMax'


@then('the response contains an error')
def step_check_error_response(context):
    data: NotFoundError = context.error.args[0]
    assert data is not None
    assert data.code == 404
    assert data.status == 'NOT_FOUND'
