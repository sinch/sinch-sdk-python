from behave import when


@when("Developer invokes a method responsible for searching available numbers with region {region} and type {number_type}")
def step_impl(context, region, number_type):
    context.available_numbers_response = context.sinch_client.numbers.list_available_numbers(
        region_code=region.strip('"'),
        number_type=number_type.strip('"')
    )
    assert context.available_numbers_response


@when("Developer invokes a method responsible for activating a first virtual phone number from the returned list of numbers")
def step_impl(context):
    context.lease_number_response = context.sinch_client.numbers.activate_number(
        phone_number=context.available_numbers_response.available_numbers[0].phone_number
    )


@when("Developer invokes a method responsible for query of a first virtual phone number from the returned list of numbers")
def step_impl(context):
    context.number_entity = context.sinch_client.numbers.search_for_number(
        phone_number=context.available_numbers_response.available_numbers[0].phone_number
    )
    assert context.number_entity


@when("Developer invokes a method responsible for searching available regions with a type {number_type}")
def step_impl(context, number_type):
    context.response = context.sinch_client.numbers.list_available_regions_for_project(
        number_type=number_type.strip('"')
    )
    assert context.response
