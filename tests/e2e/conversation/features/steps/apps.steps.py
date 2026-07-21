from behave import given, when, then
from sinch.domains.conversation.api.v1.apps_apis import Apps


@given('the Conversation service "Apps" is available')
def step_apps_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.apps, Apps), 'Apps service is not available'
    context.apps = context.sinch.conversation.apps


@when('I send a request to create an app')
def step_create_app(context):
    context.create_app_response = context.apps.create(
        display_name='E2E Conversation App',
        channel_credentials=
            {
                'SMS': {
                    'claimed_identity': 'SpaceMonkeySquadron',
                    'token': '00112233445566778899aabbccddeeff',
                },
            }
    )


@then('the conversation app is created')
def step_validate_create_app(context):
    app = context.create_app_response
    assert app is not None, 'Create app response should not be None'
    assert app.id == '01W4FFL35P4NC4K35CONVAPP001', f'Expected app.id to be "01W4FFL35P4NC4K35CONVAPP001", got "{app.id}"'
    assert app.display_name == 'E2E Conversation App', f'Expected app.display_name to be "E2E Conversation App", got "{app.display_name}"'
    assert app.channel_credentials.sms.token == '00112233445566778899aabbccddeeff', f'Expected SMS token to be "00112233445566778899aabbccddeeff", got "{app.channel_credentials.sms.token}"'
    assert app.channel_credentials.sms.claimed_identity == 'SpaceMonkeySquadron', f'Expected SMS claimed_identity to be "SpaceMonkeySquadron", got "{app.channel_credentials.sms.claimed_identity}"'
    
@when('I send a request to list all the apps')
def step_list_apps(context):
    ## Remove raw_response when sms_app_id is updated in the mock server
    response = context.apps.list(raw_response=True)
    context.apps_list = list(response.iterator())


@then('the apps list contains {count:d} apps')
def step_validate_apps_list_count(context, count):
    assert len(context.apps_list) == count, (
        f'Expected {count} apps, got {len(context.apps_list)}'
    )


@when('I send a request to retrieve an app')
def step_retrieve_app(context):
    context.app = context.apps.get(app_id='01W4FFL35P4NC4K35CONVAPP001')


@then('the response contains the app details')
def step_validate_app_details(context):
    app = context.app
    assert app is not None, 'App should not be None'
    assert app.id == '01W4FFL35P4NC4K35CONVAPP001', f'Expected app.id to be "01W4FFL35P4NC4K35CONVAPP001", got "{app.id}"'
    assert app.display_name == 'E2E Conversation App', f'Expected app.display_name to be "E2E Conversation App", got "{app.display_name}"'
    assert app.channel_credentials.sms.token == '00112233445566778899aabbccddeeff', f'Expected SMS token to be "00112233445566778899aabbccddeeff", got "{app.channel_credentials.sms.token}"'

@when('I send a request to update an app')
def step_update_app(context):
    context.update_app_response = context.apps.update(
        app_id='01W4FFL35P4NC4K35CONVAPP001',
        display_name='Updated name',
    )


@then('the response contains the app details with updated properties')
def step_validate_update_app(context):
    app = context.update_app_response
    assert app is not None, 'Update app response should not be None'
    assert app.id == '01W4FFL35P4NC4K35CONVAPP001', f'Expected app.id to be "01W4FFL35P4NC4K35CONVAPP001", got "{app.id}"'
    assert app.display_name == 'Updated name', f'Expected app.display_name to be "Updated name", got "{app.display_name}"'


@when('I send a request to delete an app')
def step_delete_app(context):
    context.delete_app_response = context.apps.delete(
        app_id='01W4FFL35P4NC4K35CONVAPP001'
    )


@then('the delete app response contains no data')
def step_validate_delete_app(context):
    assert context.delete_app_response is None, 'Delete app response should be None'
