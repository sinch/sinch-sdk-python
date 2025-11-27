from behave import given, when, then
from sinch.domains.numbers.virtual_numbers import VirtualNumbers


def count_region_type(regions, number_types):
    """Count the number of regions that have a specific number type."""
    return sum(number_types in region.types for region in regions if region.types)


@given('the Numbers service "Regions" is available')
def step_regions_service_is_available(context):
    """Ensures the Sinch client is initialized"""
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.numbers, VirtualNumbers), 'Numbers service is not available'
    context.numbers = context.sinch.numbers


@when('I send a request to list all the regions')
def step_list_all_regions(context):
    response = context.numbers.regions.list()
    context.response = response.content()


@when('I send a request to list the TOLL_FREE regions')
def step_list_toll_free_regions(context):
    response = context.numbers.regions.list(
        types=['TOLL_FREE']
    )
    context.response = response.content()


@when('I send a request to list the TOLL_FREE or MOBILE regions')
def step_list_toll_free_or_mobile_regions(context):
    response = context.numbers.regions.list(
        types=['TOLL_FREE', 'MOBILE']
    )
    context.response = response.content()


@then('the response contains "{count}" regions')
def step_check_regions_count(context, count):
    assert len(context.response) == int(count), f'Expected {count}, got {len(context.response)}'


@then('the response contains "{count}" TOLL_FREE regions')
def step_check_toll_free_regions_count(context, count):
    toll_free_count = count_region_type(context.response, 'TOLL_FREE')
    assert toll_free_count == int(count), f'Expected {count}, got {toll_free_count}'


@then('the response contains "{count}" MOBILE regions')
def step_check_mobile_regions_count(context, count):
    mobile_count = count_region_type(context.response, 'MOBILE')
    assert mobile_count == int(count), f'Expected {count}, got {mobile_count}'


@then('the response contains "{count}" LOCAL regions')
def step_check_local_regions_count(context, count):
    local_count = count_region_type(context.response, 'LOCAL')
    assert local_count == int(count), f'Expected {count}, got {local_count}'
