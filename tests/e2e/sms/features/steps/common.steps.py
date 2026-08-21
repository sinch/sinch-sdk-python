from behave import given
from sinch.domains.sms.sms import SMS

from tests.e2e.shared_config import create_test_client_with_service_plan_id


@given('the SMS service "{service_name}" is available')
def step_sms_service_available(context, service_name):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.sms, SMS), 'SMS service is not available'
    context.sms = context.sinch.sms


@given('the SMS service "{service_name}" is available and is configured for servicePlanId authentication')
def step_sms_service_available_with_service_plan(context, service_name):
    context.sinch = create_test_client_with_service_plan_id()
    assert isinstance(context.sinch.sms, SMS), 'SMS service is not available'
    context.sms = context.sinch.sms
