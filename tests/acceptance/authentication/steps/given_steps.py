from os import getenv
from behave import given


@given("an access key {key_id} obtained from Sinch portal")
def step_impl(context, key_id):
    context.key_id = getenv(key_id.strip('"'))
    assert context.key_id


@given("secret key {key_secret} obtained from Sinch portal")
def step_impl(context, key_secret):
    context.key_secret = getenv(key_secret.strip('"'))
    assert context.key_secret


@given("an access token {access_token} obtained from another instance of the SDK")
def step_impl(context, access_token):
    context.access_token = getenv(access_token.strip('"'))
    assert context.access_token


@given("the token structure has {field_name} field and data")
def step_impl(context, field_name):
    assert getattr(context.auth_token, field_name.strip('"'))


@given("the token structure has {field_name} field")
def step_impl(context, field_name):
    getattr(context.auth_token, field_name.strip('"'))
