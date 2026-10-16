from behave import given, when, then
from sinch.domains.conversation.api.v1.events_apis import Events


EVENT_ID = '01W4FFL35P4NC4K35CONVEVENT1'
APP_ID = '01W4FFL35P4NC4K35CONVAPP001'
CONTACT_ID = '01W4FFL35P4NC4K35CONTACT001'


@given('the Conversation service "Events" is available')
def step_events_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.events, Events), 'Events service is not available'
    context.events = context.sinch.conversation.events


@when('I send a request to send a conversation event to a contact')
def step_send_event(context):
    context.send_event_response = context.events.send(
        app_id=APP_ID,
        contact_id=CONTACT_ID,
        event={'composing_event': {}},
    )


@then('the response contains the id of the conversation event')
def step_validate_send_event(context):
    response = context.send_event_response
    assert response.event_id == EVENT_ID, f'Expected event_id "{EVENT_ID}", got "{response.event_id}"'
    assert response.accepted_time is not None, 'accepted_time should be set'


@when('I send a request to list the existing conversation events')
def step_list_events(context):
    context.list_response = context.events.list(
        page_size=2, contact_id=CONTACT_ID
    )
    context.events_page = context.list_response.content()


@then('the response contains "{count}" conversation events')
def step_validate_list_events(context, count):
    assert len(context.events_page) == int(count), f'Expected {count} events, got {len(context.events_page)}'


@when('I send a request to list all the conversation events')
def step_list_all_events(context):
    response = context.events.list(page_size=2, contact_id=CONTACT_ID)
    context.events_list = list(response.iterator())


@when('I iterate manually over the conversation events pages')
def step_iterate_events_pages(context):
    context.list_response = context.events.list(
        page_size=2, contact_id=CONTACT_ID
    )

    context.events_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.events_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the conversation events list contains "{count}" conversation events')
def step_validate_events_list_count(context, count):
    assert len(context.events_list) == int(count), f'Expected {count} events, got {len(context.events_list)}'


@then('the conversation events iteration result contains the data from "{count}" pages')
def step_validate_events_page_iteration_count(context, count):
    assert context.pages_iteration == int(count), f'Expected {count} pages, got {context.pages_iteration}'


@when('I send a request to retrieve a conversation event')
def step_get_event(context):
    context.get_event_response = context.events.get(event_id=EVENT_ID)


@then('the response contains the conversation event details')
def step_validate_get_event(context):
    event = context.get_event_response
    assert event.id == EVENT_ID, f'Expected id "{EVENT_ID}", got "{event.id}"'
    assert event.direction == 'TO_CONTACT', f'Unexpected direction "{event.direction}"'
    assert event.app_event.composing_event is not None, 'composing_event should be set'
    assert event.conversation_id == '01W4FFL35P4NC4K35CONVERSATI', f'Unexpected conversation_id "{event.conversation_id}"'
    assert event.contact_id == CONTACT_ID, f'Unexpected contact_id "{event.contact_id}"'
    assert event.channel_identity.channel == 'MESSENGER', f'Unexpected channel "{event.channel_identity.channel}"'
    assert event.channel_identity.identity == '7968425018576406', f'Unexpected identity "{event.channel_identity.identity}"'
    assert event.channel_identity.app_id == APP_ID, f'Unexpected app_id "{event.channel_identity.app_id}"'
    assert event.processing_mode == 'CONVERSATION', f'Unexpected processing_mode "{event.processing_mode}"'


@when('I send a request to delete a conversation event')
def step_delete_event(context):
    context.delete_event_response = context.events.delete(event_id=EVENT_ID)


@then('the delete conversation event response contains no data')
def step_validate_delete_event(context):
    assert context.delete_event_response is None, 'Delete should return no data'
