from behave import given, when, then
from sinch.domains.conversation.api.v1.event_destinations_apis import EventDestinations


EVENT_DESTINATION_ID = '01W4FFL35P4NC4K35WEBHOOK004'
APP_ID = '01W4FFL35P4NC4K35CONVAPP001'


@given('the Conversation service "Webhooks" is available')
def step_event_destinations_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.event_destinations, EventDestinations), 'Event destinations service is not available'
    context.event_destinations = context.sinch.conversation.event_destinations


@when('I send a request to create a conversation webhook')
def step_create_event_destination(context):
    context.create_event_destination_response = context.event_destinations.create(
        app_id=APP_ID,
        target='https://my-callback-server.com/capability',
        triggers=['CAPABILITY'],
        secret='CactusKnight_SurfsWaves',
        target_type='HTTP',
    )


@then('the conversation webhook is created')
def step_validate_create_event_destination(context):
    event_destination = context.create_event_destination_response
    assert event_destination.id == EVENT_DESTINATION_ID, f'Expected id "{EVENT_DESTINATION_ID}", got "{event_destination.id}"'
    assert event_destination.app_id == APP_ID, f'Expected app_id "{APP_ID}", got "{event_destination.app_id}"'
    assert event_destination.target == 'https://my-callback-server.com/capability', f'Unexpected target "{event_destination.target}"'
    assert event_destination.target_type == 'HTTP', f'Unexpected target_type "{event_destination.target_type}"'
    assert event_destination.secret == 'CactusKnight_SurfsWaves', f'Unexpected secret "{event_destination.secret}"'
    assert event_destination.triggers == ['CAPABILITY'], f'Unexpected triggers {event_destination.triggers}'
    assert event_destination.client_credentials is None, 'client_credentials should be None'


@when('I send a request to list the conversation webhooks for an app')
def step_list_event_destinations(context):
    response = context.event_destinations.list(app_id=APP_ID)
    context.event_destinations_list = list(response.iterator())


@then('the response contains the list of conversation webhooks')
def step_validate_list_event_destinations(context):
    event_destinations = context.event_destinations_list
    assert len(event_destinations) == 4, f'Expected 4 event destinations, got {len(event_destinations)}'
    entry = next(item for item in event_destinations if item.id == '01W4FFL35P4NC4K35WEBHOOK002')
    assert entry.triggers == [
        'CONTACT_CREATE',
        'CONTACT_DELETE',
        'CONTACT_IDENTITIES_DUPLICATION',
        'CONTACT_MERGE',
        'CONTACT_UPDATE',
    ], f'Unexpected triggers {entry.triggers}'
    assert entry.secret == 'DiscoDragon_BuildsLego', f'Unexpected secret "{entry.secret}"'


@when('I send a request to retrieve a conversation webhook')
def step_get_event_destination(context):
    context.event_destination = context.event_destinations.get(
        event_destination_id='01W4FFL35P4NC4K35WEBHOOK001'
    )


@then('the response contains the conversation webhook details')
def step_validate_get_event_destination(context):
    event_destination = context.event_destination
    assert event_destination.id == '01W4FFL35P4NC4K35WEBHOOK001', f'Unexpected id "{event_destination.id}"'
    assert event_destination.app_id == APP_ID, f'Unexpected app_id "{event_destination.app_id}"'
    assert event_destination.target == 'https://my-callback-server.com/unsupported', f'Unexpected target "{event_destination.target}"'
    assert event_destination.target_type == 'HTTP', f'Unexpected target_type "{event_destination.target_type}"'
    assert event_destination.secret == 'VeganVampire_SipsTea', f'Unexpected secret "{event_destination.secret}"'
    assert event_destination.triggers == ['UNSUPPORTED'], f'Unexpected triggers {event_destination.triggers}'
    credentials = event_destination.client_credentials
    assert credentials.endpoint == 'https://my-auth-server.com/oauth2/token', f'Unexpected endpoint "{credentials.endpoint}"'
    assert credentials.client_id == 'webhook-username', f'Unexpected client_id "{credentials.client_id}"'
    assert credentials.client_secret == 'webhook-password', f'Unexpected client_secret "{credentials.client_secret}"'


@when('I send a request to update a conversation webhook')
def step_update_event_destination(context):
    context.update_event_destination_response = context.event_destinations.update(
        event_destination_id=EVENT_DESTINATION_ID,
        app_id='01W4FFL35P4NC4K35CONVAPP002',
        target='https://my-callback-server.com/capability-optin-optout',
        triggers=['CAPABILITY', 'OPT_IN', 'OPT_OUT'],
        secret='SpacePanda_RidesUnicycle',
    )


@then('the response contains the conversation webhook details with updated data')
def step_validate_update_event_destination(context):
    event_destination = context.update_event_destination_response
    assert event_destination.id == EVENT_DESTINATION_ID, f'Unexpected id "{event_destination.id}"'
    assert event_destination.app_id == '01W4FFL35P4NC4K35CONVAPP002', f'Unexpected app_id "{event_destination.app_id}"'
    assert event_destination.target == 'https://my-callback-server.com/capability-optin-optout', f'Unexpected target "{event_destination.target}"'
    assert event_destination.secret == 'SpacePanda_RidesUnicycle', f'Unexpected secret "{event_destination.secret}"'
    assert event_destination.triggers == ['CAPABILITY', 'OPT_IN', 'OPT_OUT'], f'Unexpected triggers {event_destination.triggers}'


@when('I send a request to delete a conversation webhook')
def step_delete_event_destination(context):
    context.delete_event_destination_response = context.event_destinations.delete(
        event_destination_id=EVENT_DESTINATION_ID
    )


@then('the delete conversation webhook response contains no data')
def step_validate_delete_event_destination(context):
    assert context.delete_event_destination_response is None, 'Delete event destination response should be None'
