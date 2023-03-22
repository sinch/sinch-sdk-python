from behave import then


@then("the response contains list of {field_name}")
def step_impl(context, field_name):
    assert context.response
    assert hasattr(context.response, field_name.strip('"'))


@then("the response is successful and contains number details")
def step_impl(context):
    assert context.number_entity
