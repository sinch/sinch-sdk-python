from datetime import datetime, timezone
from behave import when, then
from sinch.domains.sms.models.v1.shared import MOTextMessage


@when('I send a request to retrieve an inbound message')
def step_retrieve_inbound_message(context):
    """Retrieve a single inbound message by ID"""
    context.response = context.sms.inbound_messages.get(
        inbound_id='01W4FFL35P4NC4K35INBOUND01'
    )


@then('the response contains the inbound message details')
def step_validate_inbound_message(context):
    """Validate the inbound message response"""
    data: MOTextMessage = context.response
    assert isinstance(data, MOTextMessage)
    assert data.id == '01W4FFL35P4NC4K35INBOUND01'
    assert data.from_ == '12015555555'
    assert data.to == '12017777777'
    assert data.body == 'Hello John!'
    assert data.type == 'mo_text'
    assert data.operator_id == '311071'
    assert data.received_at == datetime(2024, 6, 6, 14, 16, 54, 777000, tzinfo=timezone.utc)


@when('I send a request to list the inbound messages')
def step_list_inbound_messages(context):
    """List a page of inbound messages"""
    context.response = context.sms.inbound_messages.list(
        page_size=2,
        to=['12017777777', '12018888888']
    )


@then('the response contains "{count}" inbound messages')
def step_validate_inbound_messages_count(context, count):
    """Validate the count of inbound messages in response"""
    expected_count = int(count)
    assert len(context.response.content()) == expected_count, \
        f'Expected {expected_count}, got {len(context.response.content())}'


@when('I send a request to list all the inbound messages')
def step_list_all_inbound_messages(context):
    """List all inbound messages using iterator"""
    response = context.sms.inbound_messages.list(
        page_size=2,
        to=['12017777777', '12018888888']
    )
    inbound_messages_list = []

    for inbound_message in response.iterator():
        inbound_messages_list.append(inbound_message)

    context.inbound_messages_list = inbound_messages_list


@then('the inbound messages list contains "{count}" inbound messages')
def step_validate_inbound_messages_list_count(context, count):
    """Validate the count of inbound messages in the full list"""
    expected_count = int(count)
    assert len(context.inbound_messages_list) == expected_count, \
        f'Expected {expected_count}, got {len(context.inbound_messages_list)}'


@when('I iterate manually over the inbound messages pages')
def step_iterate_manually_inbound_messages(context):
    """Manually iterate over inbound messages pages"""
    context.list_response = context.sms.inbound_messages.list(
        page_size=2,
        to=['12017777777', '12018888888']
    )

    context.inbound_messages_list = []
    context.pages_iteration = 0
    reached_last_page = False

    while not reached_last_page:
        context.inbound_messages_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_last_page = True


@then('the inbound messages iteration result contains the data from "{count}" pages')
def step_validate_inbound_messages_pages_count(context, count):
    """Validate the count of pages in the iteration result"""
    expected_pages_count = int(count)
    assert context.pages_iteration == expected_pages_count, \
        f'Expected {expected_pages_count} pages, got {context.pages_iteration}'
