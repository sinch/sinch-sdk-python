from datetime import datetime, timezone
from behave import given, when, then
from sinch.domains.sms.models.v1.response import BatchDeliveryReport, RecipientDeliveryReport
from sinch.domains.sms.sms import SMS


@given('the SMS service "{service_name}" is available')
def step_sms_service_available(context, service_name):
    """Ensures the Sinch client is initialized"""
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.sms, SMS), 'SMS service is not available'
    context.sms = context.sinch.sms


@given('the SMS service "{service_name}" is available and is configured for servicePlanId authentication')
def step_sms_service_available_with_service_plan(context, service_name):
    """Ensures the Sinch client is initialized with service_plan_id authentication"""
    from sinch import SinchClient
    
    # Create a new client with service_plan_id authentication
    context.sinch = SinchClient(
        service_plan_id='CappyPremiumPlan',
        sms_api_token='HappyCappyToken',
    )
    context.sinch.configuration.auth_origin = 'http://localhost:3011'
    context.sinch.configuration.sms_origin = 'http://localhost:3017'
    context.sinch.configuration.sms_origin_with_service_plan_id = 'http://localhost:3017'
    assert isinstance(context.sinch.sms, SMS), 'SMS service is not available'
    context.sms = context.sinch.sms


@when('I send a request to retrieve a summary SMS delivery report')
def step_retrieve_summary_delivery_report(context):
    """Retrieve a summary SMS delivery report"""
    context.response = context.sms.delivery_reports.get(
        batch_id='01W4FFL35P4NC4K35SMSBATCH1',
        status=['DELIVERED', 'FAILED'],
        code=[15, 0]
    )


@then('the response contains a summary SMS delivery report')
def step_validate_summary_delivery_report(context):
    """Validate summary SMS delivery report response"""
    data: BatchDeliveryReport = context.response
    assert data.batch_id == '01W4FFL35P4NC4K35SMSBATCH1'
    assert data.client_reference == 'reference_e2e'
    assert data.statuses is not None
    assert len(data.statuses) >= 2
    
    status = data.statuses[0]
    assert status.code == 15
    assert status.count == 1
    assert status.recipients is None
    assert status.status == 'Failed'
    
    status = data.statuses[1]
    assert status.code == 0
    assert status.count == 1
    assert status.recipients is None
    assert status.status == 'Delivered'
    
    assert data.total_message_count == 2
    assert data.type == 'delivery_report_sms'


@when('I send a request to retrieve a full SMS delivery report')
def step_retrieve_full_delivery_report(context):
    """Retrieve a full SMS delivery report"""
    context.response = context.sms.delivery_reports.get(
        batch_id='01W4FFL35P4NC4K35SMSBATCH1',
        report_type='full'
    )


@then('the response contains a full SMS delivery report')
def step_validate_full_delivery_report(context):
    """Validate full SMS delivery report response"""
    data: BatchDeliveryReport = context.response
    assert data.batch_id == '01W4FFL35P4NC4K35SMSBATCH1'
    assert data.statuses is not None
    status = data.statuses[0]
    assert status.recipients is not None
    assert status.code == 0
    assert status.count == 1
    assert status.recipients[0] == '12017777777'
    assert status.status == 'Delivered'


@when('I send a request to retrieve a recipient\'s delivery report')
def step_retrieve_recipient_delivery_report(context):
    """Retrieve a recipient's delivery report"""
    context.response = context.sms.delivery_reports.get_for_number(
        batch_id='01W4FFL35P4NC4K35SMSBATCH1',
        recipient='12017777777'
    )


@then('the response contains the recipient\'s delivery report details')
def step_validate_recipient_delivery_report(context):
    """Validate recipient delivery report response"""
    data: RecipientDeliveryReport = context.response
    assert data.batch_id == '01W4FFL35P4NC4K35SMSBATCH1'
    assert data.recipient == '12017777777'
    assert data.client_reference == 'reference_e2e'
    assert data.status == 'Delivered'
    assert data.type == 'recipient_delivery_report_sms'
    assert data.code == 0
    assert data.at == datetime(2024, 6, 6, 13, 6, 27, 833000, tzinfo=timezone.utc)
    assert data.operator_status_at == datetime(2024, 6, 6, 13, 6, 0, tzinfo=timezone.utc)


@when('I send a request to list the SMS delivery reports')
def step_list_delivery_reports(context):
    """List a page of SMS delivery reports"""
    context.response = context.sms.delivery_reports.list()


@then('the response contains "{count}" SMS delivery reports')
def step_validate_delivery_reports_count(context, count):
    """Validate the count of SMS delivery reports in response"""
    expected_count = int(count)
    assert len(context.response.content()) == expected_count, \
        f'Expected {expected_count}, got {len(context.response.content())}'


@when('I send a request to list all the SMS delivery reports')
def step_list_all_delivery_reports(context):
    """List all SMS delivery reports using iterator"""
    response = context.sms.delivery_reports.list(page_size=2)
    delivery_reports_list = []
    
    for delivery_report in response.iterator():
        delivery_reports_list.append(delivery_report)
    
    context.delivery_reports_list = delivery_reports_list


@then('the SMS delivery reports list contains "{count}" SMS delivery reports')
def step_validate_delivery_reports_list_count(context, count):
    """Validate the count of SMS delivery reports in the full list"""
    expected_count = int(count)
    assert len(context.delivery_reports_list) == expected_count, \
        f'Expected {expected_count}, got {len(context.delivery_reports_list)}'


@when('I iterate manually over the SMS delivery reports pages')
def step_iterate_manually_delivery_reports(context):
    """Manually iterate over SMS delivery reports pages"""
    context.list_response = context.sms.delivery_reports.list(page_size=2)
    
    # Iterate through all pages
    context.delivery_reports_list = []
    context.pages_iteration = 0
    reached_last_page = False
    
    while not reached_last_page:
        context.delivery_reports_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_last_page = True


@then('the SMS delivery reports iteration result contains the data from "{count}" pages')
def step_validate_delivery_reports_pages_count(context, count):
    """Validate the count of pages in the iteration result"""
    expected_pages_count = int(count)
    assert context.pages_iteration == expected_pages_count, \
        f'Expected {expected_pages_count} pages, got {context.pages_iteration}'
