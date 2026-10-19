from datetime import datetime, timezone
from behave import given, when, then
from sinch.domains.conversation.api.v1.conversations_apis import Conversations


APP_ID = '01W4FFL35P4NC4K35CONVAPP001'
CONTACT_ID = '01W4FFL35P4NC4K35CONTACT001'
CONVERSATION_ID = '01W4FFL35P4NC4K35CONVERS001'


@given('the Conversation service "Conversations" is available')
def step_conversations_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.conversations, Conversations), 'Conversations service is not available'
    context.conversations = context.sinch.conversation.conversations


@when('I send a request to create a conversation')
def step_create_conversation(context):
    context.conversation = context.conversations.create(
        app_id=APP_ID,
        contact_id=CONTACT_ID,
        active=True,
        active_channel='MESSENGER',
        metadata_json={'prop1': 'value1', 'prop2': 'value2'},
    )


@then('the conversation is created')
def step_validate_created_conversation(context):
    conversation = context.conversation
    assert conversation.id == CONVERSATION_ID, f'Expected id to be "{CONVERSATION_ID}", got "{conversation.id}"'
    assert conversation.app_id == APP_ID, f'Expected app_id to be "{APP_ID}", got "{conversation.app_id}"'
    assert conversation.contact_id == CONTACT_ID, f'Expected contact_id to be "{CONTACT_ID}", got "{conversation.contact_id}"'
    assert conversation.active is True, f'Expected active to be True, got {conversation.active}'
    assert conversation.active_channel == 'CHANNEL_UNSPECIFIED', f'Expected active_channel to be "CHANNEL_UNSPECIFIED", got "{conversation.active_channel}"'
    assert conversation.metadata_json == {'prop1': 'value1', 'prop2': 'value2'}, f'Unexpected metadata_json: {conversation.metadata_json}'
    expected_last_received = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert conversation.last_received == expected_last_received, f'Expected last_received to be {expected_last_received}, got {conversation.last_received}'


@when('I send a request to list the existing conversations')
def step_list_conversations(context):
    context.list_response = context.conversations.list(
        app_id=APP_ID, page_size=2
    )
    context.conversations_page = context.list_response.content()


@then('the response contains "{count}" conversations')
def step_validate_list_conversations(context, count):
    assert len(context.conversations_page) == int(count), f'Expected {count} conversations, got {len(context.conversations_page)}'


@when('I send a request to list all the conversations')
def step_list_all_conversations(context):
    response = context.conversations.list(app_id=APP_ID, page_size=2)
    context.conversations_list = list(response.iterator())


@when('I iterate manually over the conversations pages')
def step_iterate_conversations_pages(context):
    context.list_response = context.conversations.list(
        app_id=APP_ID, page_size=2
    )
    context.conversations_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.conversations_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the conversations list contains "{count}" conversations')
def step_validate_conversations_list_count(context, count):
    assert len(context.conversations_list) == int(count), f'Expected {count} conversations, got {len(context.conversations_list)}'


@then('the conversations iteration result contains the data from "{count}" pages')
def step_validate_conversations_page_iteration_count(context, count):
    assert context.pages_iteration == int(count), f'Expected {count} pages, got {context.pages_iteration}'


@when('I send a request to retrieve a conversation')
def step_retrieve_conversation(context):
    context.conversation = context.conversations.get(
        conversation_id=CONVERSATION_ID
    )


@then('the response contains the conversation details')
def step_validate_conversation_details(context):
    conversation = context.conversation
    assert conversation.id == CONVERSATION_ID, f'Expected id to be "{CONVERSATION_ID}", got "{conversation.id}"'
    assert conversation.app_id == APP_ID, f'Expected app_id to be "{APP_ID}", got "{conversation.app_id}"'
    assert conversation.contact_id == '01W4FFL35P4NC4K35CONTACT002', f'Expected contact_id to be "01W4FFL35P4NC4K35CONTACT002", got "{conversation.contact_id}"'
    expected_last_received = datetime(2024, 6, 6, 14, 42, 42, tzinfo=timezone.utc)
    assert conversation.last_received == expected_last_received, f'Expected last_received to be {expected_last_received}, got {conversation.last_received}'
    assert conversation.active_channel == 'MESSENGER', f'Expected active_channel to be "MESSENGER", got "{conversation.active_channel}"'
    assert conversation.active is True, f'Expected active to be True, got {conversation.active}'
    assert conversation.metadata == 'e2e tests', f'Expected metadata to be "e2e tests", got "{conversation.metadata}"'
    assert conversation.metadata_json == {'prop1': 'value1', 'prop2': 'value2'}, f'Unexpected metadata_json: {conversation.metadata_json}'
    assert conversation.correlation_id == '', f'Expected correlation_id to be "", got "{conversation.correlation_id}"'


@when('I send a request to update a conversation')
def step_update_conversation(context):
    context.conversation = context.conversations.update(
        conversation_id=CONVERSATION_ID,
        active=False,
        app_id='01W4FFL35P4NC4K35CONVAPP002',
        correlation_id='my-correlator',
    )


@then('the response contains the conversation details with updated data')
def step_validate_updated_conversation(context):
    conversation = context.conversation
    assert conversation.id == CONVERSATION_ID, f'Expected id to be "{CONVERSATION_ID}", got "{conversation.id}"'
    assert conversation.app_id == '01W4FFL35P4NC4K35CONVAPP002', f'Expected app_id to be "01W4FFL35P4NC4K35CONVAPP002", got "{conversation.app_id}"'
    assert conversation.active is False, f'Expected active to be False, got {conversation.active}'
    assert conversation.metadata == 'Transferred conversation', f'Expected metadata to be "Transferred conversation", got "{conversation.metadata}"'
    assert conversation.correlation_id == 'my-correlator', f'Expected correlation_id to be "my-correlator", got "{conversation.correlation_id}"'


@when('I send a request to delete a conversation')
def step_delete_conversation(context):
    context.delete_conversation_response = context.conversations.delete(
        conversation_id=CONVERSATION_ID
    )


@then('the delete conversation response contains no data')
def step_validate_delete_conversation_response(context):
    assert context.delete_conversation_response is None, 'Delete conversation response should be None'


@when('I send a request to list the recent conversations')
def step_list_recent_conversations(context):
    context.list_response = context.conversations.list_recent(
        app_id=APP_ID, page_size=2
    )
    context.recent_conversations_page = context.list_response.content()


@then('the response contains "{count}" recent conversations')
def step_validate_list_recent_conversations(context, count):
    assert len(context.recent_conversations_page) == int(count), f'Expected {count} recent conversations, got {len(context.recent_conversations_page)}'
    recent = context.recent_conversations_page[0]
    assert recent.conversation.id == CONVERSATION_ID, f'Expected conversation id to be "{CONVERSATION_ID}", got "{recent.conversation.id}"'
    assert recent.last_message.id == '01W4FFL35P4NC4K35MESSAGE001', f'Expected last_message id to be "01W4FFL35P4NC4K35MESSAGE001", got "{recent.last_message.id}"'
    assert recent.last_message.app_message.text_message.text == '🦜: test', f'Unexpected last_message text: {recent.last_message.app_message.text_message.text}'


@when('I send a request to list all the recent conversations')
def step_list_all_recent_conversations(context):
    response = context.conversations.list_recent(app_id=APP_ID, page_size=2)
    context.recent_conversations_list = list(response.iterator())


@when('I iterate manually over the recent conversations pages')
def step_iterate_recent_conversations_pages(context):
    context.list_response = context.conversations.list_recent(
        app_id=APP_ID, page_size=2
    )
    context.recent_conversations_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.recent_conversations_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the recent conversations list contains "{count}" recent conversations')
def step_validate_recent_conversations_list_count(context, count):
    assert len(context.recent_conversations_list) == int(count), f'Expected {count} recent conversations, got {len(context.recent_conversations_list)}'


@then('the recent conversations iteration result contains the data from "{count}" pages')
def step_validate_recent_conversations_page_iteration_count(context, count):
    assert context.pages_iteration == int(count), f'Expected {count} pages, got {context.pages_iteration}'


@when('I send a request to inject an event into a conversation')
def step_inject_event(context):
    context.inject_event_response = context.conversations.inject_event(
        conversation_id=CONVERSATION_ID,
        app_event={'composing_event': {}},
        accept_time=datetime.now(timezone.utc),
    )


@then('the event is created and injected in the conversation')
def step_validate_injected_event(context):
    response = context.inject_event_response
    assert response.event_id == '01W4FFL35P4NC4K35CONVEVENT1', f'Expected event_id to be "01W4FFL35P4NC4K35CONVEVENT1", got "{response.event_id}"'
    expected_accepted_time = datetime(2024, 6, 6, 15, 15, 15, tzinfo=timezone.utc)
    assert response.accepted_time == expected_accepted_time, f'Expected accepted_time to be {expected_accepted_time}, got {response.accepted_time}'


@when('I send a request to inject a message into a conversation')
def step_inject_message(context):
    context.inject_message_response = context.conversations.inject_message(
        conversation_id=CONVERSATION_ID,
        contact_id='01W4FFL35P4NC4K35CONTACT002',
        channel_identity={
            'channel': 'MESSENGER',
            'identity': '7968425018576406',
            'app_id': APP_ID,
        },
        direction='TO_CONTACT',
        accept_time=datetime.now(timezone.utc),
        app_message={'text_message': {'text': 'Injected text message'}},
    )


@then('the message is created and injected in the conversation')
def step_validate_injected_message(context):
    assert context.inject_message_response is None, 'Inject message response should be None'


@when('I send a request to stop a conversation')
def step_stop_conversation(context):
    context.stop_conversation_response = context.conversations.stop_active(
        conversation_id=CONVERSATION_ID
    )


@then('the stop conversation response contains no data')
def step_validate_stop_conversation_response(context):
    assert context.stop_conversation_response is None, 'Stop conversation response should be None'
