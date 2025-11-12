from datetime import datetime, timezone
from behave import given, when, then
from sinch.domains.sms.models.v1.types import BatchResponse
from sinch.domains.sms.models.v1.response.dry_run_response import DryRunResponse
from sinch.domains.sms.models.v1.shared.text_response import TextResponse


def _setup_sinch_client(context, use_service_plan_auth=False):
    """Helper function to setup Sinch client"""
    from sinch import SinchClient
    
    if use_service_plan_auth:
        sinch = SinchClient(
            service_plan_id='CappyPremiumPlan',
            sms_api_token='HappyCappyToken',
        )
        sinch.configuration.sms_origin_with_service_plan_id = 'http://localhost:3017'
    else:
        sinch = SinchClient(
            project_id='tinyfrog-jump-high-over-lilypadbasin',
            key_id='keyId',
            key_secret='keySecret',
        )
    
    sinch.configuration.auth_origin = 'http://localhost:3011'
    sinch.configuration.sms_origin = 'http://localhost:3017'
    
    context.sinch = sinch
    context.sms = sinch.sms


@given('the SMS service "Batches" is available')
def step_sms_service_batches_available(context):
    """Ensures the Sinch client is initialized"""
    _setup_sinch_client(context, use_service_plan_auth=False)


@given('the SMS service "Batches" is available and is configured for servicePlanId authentication')
def step_sms_service_batches_available_with_service_plan(context):
    """Ensures the Sinch client is initialized with service_plan_id authentication"""
    _setup_sinch_client(context, use_service_plan_auth=True)


@when('I send a request to send a text message')
def step_send_text_message(context):
    """Send a text message"""
    context.response = context.sms.send_sms_batch(
        body='SMS body message',
        to=['+12017777777'],
        from_='+12015555555',
        send_at=datetime(2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc),
        delivery_report='full',
        feedback_enabled=True,
    )


@then('the response contains the text SMS details')
def step_validate_text_sms_details(context):
    """Validate text SMS response"""
    data: BatchResponse = context.response
    assert data.id == '01W4FFL35P4NC4K35SMSBATCH1'
    assert data.to == ['12017777777']
    assert data.from_ == '12015555555'
    assert data.canceled is False
    assert data.body == 'SMS body message'
    assert data.type == 'mt_text'
    assert data.created_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert data.modified_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert data.delivery_report == 'full'
    assert data.send_at == datetime(2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc)
    assert data.expire_at == datetime(2024, 6, 9, 9, 25, 0, tzinfo=timezone.utc)
    assert data.feedback_enabled is True
    assert isinstance(data, TextResponse)
    assert data.flash_message is False


@when('I send a request to send a text message with multiple parameters')
def step_send_text_message_with_parameters(context):
    """Send a text message with multiple parameters"""
    context.response = context.sms.send_sms_batch(
        body='Hello ${name}! Get 20% off with this discount code ${code}',
        to=['+12017777777', '+12018888888'],
        from_='+12015555555',
        parameters={
            'name': {
                '+12017777777': 'John',
                '+12018888888': 'Paul',
                'default': 'there',
            },
            'code': {
                '+12017777777': 'HALLOWEEN20 🎃',
            },
        },
        delivery_report='full',
    )


@then('the response contains the text SMS details with multiple parameters')
def step_validate_text_sms_with_parameters(context):
    """Validate text SMS response with parameters"""
    data: BatchResponse = context.response
    assert data.id == '01W4FFL35P4NC4K35SMSBATCH2'
    assert data.to == ['12017777777', '12018888888']
    assert data.from_ == '12015555555'
    assert data.canceled is False
    
    expected_parameters = {
        'name': {
            'default': 'there',
            '+12017777777': 'John',
            '+12018888888': 'Paul',
        },
        'code': {
            '+12017777777': 'HALLOWEEN20 🎃',
        },
    }
    assert data.parameters == expected_parameters
    assert data.body == 'Hello ${name}! Get 20% off with this discount code ${code}'
    assert data.type == 'mt_text'
    assert data.created_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert data.modified_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert data.delivery_report == 'full'
    assert data.expire_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert isinstance(data, TextResponse)
    assert data.flash_message is False


@when('I send a request to perform a dry run of a batch')
def step_perform_dry_run(context):
    """Perform a dry run of a batch"""
    context.dry_run_response = context.sms.batches.dry_run_sms(
        from_='+12015555555',
        to=[
            '+12017777777',
            '+12018888888',
            '+12019999999',
        ],
        parameters={
            'name': {
                '+12017777777': 'John',
                'default': 'there',
            },
        },
        body='Hello ${name}!',
        delivery_report='none',
    )


@then('the response contains the calculated bodies and number of parts for all messages in the batch')
def step_validate_dry_run_response(context):
    """Validate dry run response"""
    data: DryRunResponse = context.dry_run_response
    assert data.number_of_messages == 3
    assert data.number_of_recipients == 3
    assert data.per_recipient is not None
    assert len(data.per_recipient) == 3
    
    john_message = next(
        (msg for msg in data.per_recipient if msg.recipient == '12017777777'),
        None
    )
    assert john_message is not None
    assert john_message.body == 'Hello John!'
    assert john_message.number_of_parts == 1
    assert john_message.encoding == 'text'
    
    default_message = next(
        (msg for msg in data.per_recipient if msg.recipient == '12018888888'),
        None
    )
    assert default_message is not None
    assert default_message.body == 'Hello there!'
    assert default_message.number_of_parts == 1
    assert default_message.encoding == 'text'


@when('I send a request to list the SMS batches')
def step_list_sms_batches(context):
    """List SMS batches"""
    context.response = context.sms.batches.list(
        page_size=2,
    )


@then('the response contains "{count}" SMS batches')
def step_validate_batches_count(context, count):
    """Validate the count of SMS batches in response"""
    expected_count = int(count)
    assert len(context.response.content()) == expected_count, \
        f'Expected {expected_count}, got {len(context.response.content())}'


@when('I send a request to list all the SMS batches')
def step_list_all_sms_batches(context):
    """List all SMS batches using iterator"""
    response = context.sms.batches.list(page_size=2)
    batches_list = []
    
    for batch in response.iterator():
        batches_list.append(batch)
    
    context.batches_list = batches_list


@when('I iterate manually over the SMS batches pages')
def step_iterate_manually_batches(context):
    """Manually iterate over SMS batches pages"""
    context.list_response = context.sms.batches.list(
        page_size=2,
    )
    
    context.batches_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False
    
    while not reached_end_of_pages:
        context.batches_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the SMS batches list contains "{count}" SMS batches')
def step_validate_batches_list_count(context, count):
    """Validate the count of SMS batches in the full list"""
    expected_count = int(count)
    assert len(context.batches_list) == expected_count, \
        f'Expected {expected_count}, got {len(context.batches_list)}'


@then('the SMS batches iteration result contains the data from "{count}" pages')
def step_validate_batches_pages_count(context, count):
    """Validate the count of pages in the iteration result"""
    expected_pages_count = int(count)
    assert context.pages_iteration == expected_pages_count, \
        f'Expected {expected_pages_count} pages, got {context.pages_iteration}'


@when('I send a request to retrieve an SMS batch')
def step_retrieve_sms_batch(context):
    """Retrieve an SMS batch"""
    context.batch = context.sms.batches.get(
        batch_id='01W4FFL35P4NC4K35SMSBATCH1',
    )


@then('the response contains the SMS batch details')
def step_validate_batch_details(context):
    """Validate SMS batch response"""
    batch: BatchResponse = context.batch
    assert batch.id == '01W4FFL35P4NC4K35SMSBATCH1'
    assert batch.to == ['12017777777']
    assert batch.from_ == '12015555555'
    assert batch.canceled is False
    assert batch.body == 'SMS body message'
    assert batch.type == 'mt_text'
    assert batch.created_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert batch.modified_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert batch.delivery_report == 'full'
    assert batch.send_at == datetime(2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc)
    assert batch.expire_at == datetime(2024, 6, 9, 9, 25, 0, tzinfo=timezone.utc)
    assert batch.feedback_enabled is True
    assert isinstance(batch, TextResponse)
    assert batch.flash_message is False


@when('I send a request to update an SMS batch')
def step_update_sms_batch(context):
    """Update an SMS batch"""
    context.batch = context.sms.batches.update_sms(
        batch_id='01W4FFL35P4NC4K35SMSBATCH1',
        from_='+12016666666',
        to_add=[
            '01W4FFL35P4NC4K35SMSGROUP1',
        ],
        delivery_report='summary',
    )


@then('the response contains the SMS batch details with updated data')
def step_validate_updated_batch_details(context):
    """Validate updated SMS batch response"""
    batch: BatchResponse = context.batch
    assert batch.id == '01W4FFL35P4NC4K35SMSBATCH1'
    assert batch.to == ['12017777777', '01W4FFL35P4NC4K35SMSGROUP1']
    assert batch.from_ == '12016666666'
    assert batch.canceled is False
    assert batch.body == 'SMS body message'
    assert batch.type == 'mt_text'
    assert batch.created_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert batch.modified_at == datetime(2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc)
    assert batch.delivery_report == 'summary'
    assert batch.send_at == datetime(2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc)
    assert batch.expire_at == datetime(2024, 6, 9, 9, 25, 0, tzinfo=timezone.utc)
    assert batch.feedback_enabled is True
    assert isinstance(batch, TextResponse)
    assert batch.flash_message is False


@when('I send a request to replace an SMS batch')
def step_replace_sms_batch(context):
    """Replace an SMS batch"""
    context.batch = context.sms.batches.replace_sms(
        batch_id='01W4FFL35P4NC4K35SMSBATCH1',
        from_='+12016666666',
        to=['+12018888888'],
        body='This is the replacement batch',
        send_at=datetime(2024, 6, 6, 9, 35, 0, tzinfo=timezone.utc),
    )


@then('the response contains the new SMS batch details with the provided data for replacement')
def step_validate_replaced_batch_details(context):
    """Validate replaced SMS batch response"""
    batch: BatchResponse = context.batch
    assert batch.id == '01W4FFL35P4NC4K35SMSBATCH1'
    assert batch.to == ['12018888888']
    assert batch.from_ == '12016666666'
    assert batch.canceled is False
    assert batch.body == 'This is the replacement batch'
    assert batch.type == 'mt_text'
    assert batch.created_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert batch.modified_at == datetime(2024, 6, 6, 9, 23, 32, 504000, tzinfo=timezone.utc)
    assert batch.delivery_report == 'none'
    assert batch.send_at == datetime(2024, 6, 6, 9, 35, 0, tzinfo=timezone.utc)
    assert batch.expire_at == datetime(2024, 6, 9, 9, 35, 0, tzinfo=timezone.utc)
    assert batch.feedback_enabled is False
    assert isinstance(batch, TextResponse)
    assert batch.flash_message is False


@when('I send a request to cancel an SMS batch')
def step_cancel_sms_batch(context):
    """Cancel an SMS batch"""
    context.batch = context.sms.batches.cancel(
        batch_id='01W4FFL35P4NC4K35SMSBATCH1',
    )


@then('the response contains the SMS batch details with a cancelled status')
def step_validate_cancelled_batch(context):
    """Validate cancelled SMS batch response"""
    batch: BatchResponse = context.batch
    assert batch.id == '01W4FFL35P4NC4K35SMSBATCH1'
    assert batch.canceled is True


@when('I send a request to send delivery feedbacks')
def step_send_delivery_feedback(context):
    """Send delivery feedback"""
    context.delivery_feedback_response = context.sms.batches.send_delivery_feedback(
        batch_id='01W4FFL35P4NC4K35SMSBATCH1',
        recipients=[
            '+12017777777',
        ],
    )


@then('the delivery feedback response contains no data')
def step_validate_delivery_feedback_response(context):
    """Validate delivery feedback response"""
    assert context.delivery_feedback_response is None
