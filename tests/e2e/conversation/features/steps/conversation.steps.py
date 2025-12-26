from datetime import datetime, timezone
from behave import given, when, then
from sinch.domains.conversation.api.v1.messages_apis import Messages


@given('the Conversation service "Messages" is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.messages, Messages), 'Messages service is not available'
    context.messages = context.sinch.conversation.messages


@when('I send a request to delete a message')
def step_delete_message(context):
    context.delete_message_response = context.messages.delete(
        message_id='01W4FFL35P4NC4K35MESSAGE001'
    )


@then('the delete message response contains no data')
def step_validate_delete_message_response(context):
    assert context.delete_message_response is None, 'Delete message response should be None'


@when('I send a request to retrieve a message')
def step_retrieve_message(context):
    context.message = context.messages.get(
        message_id='01W4FFL35P4NC4K35MESSAGE001'
    )


@then('the response contains the message details')
def step_validate_message_details(context):
    message = context.message
    assert message is not None, 'Message should not be None'
    assert message.id == '01W4FFL35P4NC4K35MESSAGE001', f'Expected message.id to be "01W4FFL35P4NC4K35MESSAGE001", got "{message.id}"'
    assert message.direction == 'TO_CONTACT', f'Expected message.direction to be "TO_CONTACT", got "{message.direction}"'
    assert message.conversation_id == '01W4FFL35P4NC4K35CONVERSATI', f'Expected message.conversation_id to be "01W4FFL35P4NC4K35CONVERSATI", got "{message.conversation_id}"'
    assert message.contact_id == '01W4FFL35P4NC4K35CONTACT001', f'Expected message.contact_id to be "01W4FFL35P4NC4K35CONTACT001", got "{message.contact_id}"'
    assert message.metadata == '', f'Expected message.metadata to be "", got "{message.metadata}"'
    
    expected_accept_time = datetime(2024, 6, 6, 12, 42, 42, tzinfo=timezone.utc)
    assert message.accept_time == expected_accept_time, f'Expected message.accept_time to be {expected_accept_time}, got {message.accept_time}'
    
    assert message.processing_mode == 'CONVERSATION', f'Expected message.processing_mode to be "CONVERSATION", got "{message.processing_mode}"'
    assert message.injected is False, f'Expected message.injected to be False, got {message.injected}'
    
    assert message.channel_identity is not None, 'Message channel_identity should not be None'
    assert message.channel_identity.channel == 'SMS', f'Expected channel_identity.channel to be "SMS", got "{message.channel_identity.channel}"'
    assert message.channel_identity.identity == '12015555555', f'Expected channel_identity.identity to be "12015555555", got "{message.channel_identity.identity}"'
    assert message.channel_identity.app_id == '', f'Expected channel_identity.app_id to be "", got "{message.channel_identity.app_id}"'


@when('I send a request to update a message')
def step_update_message(context):
    context.update_message_response = context.messages.update(
        message_id='01W4FFL35P4NC4K35MESSAGE001',
        metadata='Updated metadata'
    )


@then('the response contains the message details with updated metadata')
def step_validate_update_message_response(context):
    message = context.update_message_response
    assert message is not None, 'Update message response should not be None'
    assert message.id == '01W4FFL35P4NC4K35MESSAGE001', f'Expected message.id to be "01W4FFL35P4NC4K35MESSAGE001", got "{message.id}"'
    assert message.metadata == 'Updated metadata', f'Expected message.metadata to be "Updated metadata", got "{message.metadata}"'


@when('I send a request to send a message to a contact')
def step_send_message(context):
    pass


@then('the response contains the id of the message')
def step_validate_send_message_response(context):
    pass


@when('I send a request to list the existing messages')
def step_list_messages(context):
    pass


@then('the response contains "{count}" messages')
def step_validate_message_count(context, count):
    pass


@when('I send a request to list all the messages')
def step_list_all_messages(context):
    pass


@then('the messages list contains "{count}" messages')
def step_validate_total_message_count(context, count):
    pass


@when('I iterate manually over the messages pages')
def step_iterate_messages_pages(context):
    pass


@then('the result contains the data from "{count}" pages')
def step_validate_page_count(context, count):
    pass
