from behave import when
from sinch import Sinch


@when("developer initialize Sinch SDK using token received from the Key Distribution Center or other source")
def step_impl(context):
    pass


@when("developer initialize Sinch SDK using the invalid token")
def step_impl(context):
    raise NotImplementedError(u'STEP: When developer initialize Sinch SDK using the invalid token')


@when("developer initialize Sinch SDK using credentials obtained from Sinch portal")
def step_impl(context):
    context.sinch_instance = Sinch(key_id=context.key_id, key_secret=context.key_secret)
    assert context.sinch_instance


@when("developer initialize Sinch SDK using invalid credentials")
def step_impl(context):
    context.sinch_instance = Sinch(key_id="Spanish", key_secret="Inquisition")
    assert context.sinch_instance
