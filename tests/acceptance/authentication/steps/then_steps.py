from sinch.core.exceptions import SinchAuthenticationException
from behave import then


@then("the Sinch SDK accepts and processes the token without reporting any issues")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the Sinch SDK accepts and processes the token without reporting any issues')


@then("the Sinch SDK rejects the token and raises an error")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the Sinch SDK rejects the token and raises an error')


@then("developer is able to retrieve token using Sinch SDK")
def step_impl(context):
    context.auth_token = context.sinch_instance.get_auth_token()
    assert context.auth_token


@then("the Sinch SDK tries to acquire the token and raises an error")
def step_impl(context):
    try:
        context.auth_token = context.sinch_instance.get_auth_token()
    except SinchAuthenticationException:
        pass
