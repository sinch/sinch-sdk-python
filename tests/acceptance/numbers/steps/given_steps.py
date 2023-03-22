import os
from behave import given

from sinch import Client


@given("an access key KEY_ID obtained from Sinch portal")
def step_impl(context):
    context.key_id = os.getenv("KEY_ID")


@given("secret key KEY_SECRET obtained from Sinch portal")
def step_impl(context):
    context.key_secret = os.getenv("KEY_SECRET")


@given("project id PROJECT_ID obtained from Sinch portal")
def step_impl(context):
    context.project_id = os.getenv("PROJECT_ID")


@given("Sinch SDK client is configured with NUMBERS_URL and AUTHENTICATION_URL environment variables")
def step_impl(context):
    context.sinch_client = Client(
        key_id=context.key_id,
        key_secret=context.key_secret,
        project_id=context.project_id
    )
    numbers_url = os.getenv("NUMBERS_URL")
    authentication_url = os.getenv("AUTHENTICATION_URL")

    if numbers_url:
        context.sinch_client.configuration.numbers_origin = numbers_url
        context.sinch_client.configuration.disable_https = True

    if authentication_url:
        context.sinch_client.configuration.auth_origin = authentication_url
        context.sinch_client.configuration.disable_https = True


@given("the number entity contains {field} field and data")
def step_impl(context, field):
    assert hasattr(context.number_entity, field.strip('"'))


@given("the region entity contains {field} field and data")
def step_impl(context, field):
    assert hasattr(context.response.available_regions[0], field.strip('"'))
