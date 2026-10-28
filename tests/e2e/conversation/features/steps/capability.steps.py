from behave import given, when, then
from sinch.domains.conversation.api.v1.capability_apis import Capability


@given('the Conversation service "Capability" is available')
def step_capability_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.capability, Capability), 'Capability service is not available'
    context.capability = context.sinch.conversation.capability


@when('I send a request to query a capability lookup')
def step_lookup_capability(context):
    context.lookup_capability_response = context.capability.lookup(
        app_id='01W4FFL35P4NC4K35CONVAPP001',
        contact_id='01W4FFL35P4NC4K35CONTACT001'
    )


@then('the response contains the id of the capability lookup query')
def step_validate_lookup_capability(context):
    response = context.lookup_capability_response
    assert response is not None, 'Lookup capability response should not be None'
    assert response.app_id == '01W4FFL35P4NC4K35CONVAPP001', f'Expected app_id "01W4FFL35P4NC4K35CONVAPP001", got "{response.app_id}"'
    assert response.recipient.contact_id == '01W4FFL35P4NC4K35CONTACT001', f'Expected recipient.contact_id "01W4FFL35P4NC4K35CONTACT001", got "{response.recipient.contact_id}"'
    assert response.request_id == '01W4FFL35P4NC4K35CAPABILITY', f'Expected request_id "01W4FFL35P4NC4K35CAPABILITY", got "{response.request_id}"'
