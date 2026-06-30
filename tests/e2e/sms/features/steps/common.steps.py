from behave import given
from sinch.domains.sms.sms import SMS


@given('the SMS service "{service_name}" is available')
def step_sms_service_available(context, service_name):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.sms, SMS), 'SMS service is not available'
    context.sms = context.sinch.sms


@given('the SMS service "{service_name}" is available and is configured for servicePlanId authentication')
def step_sms_service_available_with_service_plan(context, service_name):
    from sinch import SinchClient

    context.sinch = SinchClient(
        service_plan_id='CappyPremiumPlan',
        sms_api_token='HappyCappyToken',
    )
    context.sinch.configuration.auth_origin = 'http://localhost:3011'
    context.sinch.configuration.sms_origin = 'http://localhost:3017'
    context.sinch.configuration.sms_origin_with_service_plan_id = 'http://localhost:3017'
    assert isinstance(context.sinch.sms, SMS), 'SMS service is not available'
    context.sms = context.sinch.sms
