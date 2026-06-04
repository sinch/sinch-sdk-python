from behave import when, then
from datetime import datetime, timezone


@when('I send a request to create an SMS group')
def step_create_sms_group(context):
    context.response = context.sms.groups.create(
        name='Group master',
        members=['+12017778888', '+12018887777'],
        child_groups=['01W4FFL35P4NC4K35SUBGROUP1'],
    )

@when('I send a request to retrieve an SMS group')
def step_retrieve_sms_group(context):
    context.response = context.sms.groups.get(
        group_id='01W4FFL35P4NC4K35SMSGROUP1'
    )



@then('the response contains the SMS group details')
def step_validate_sms_group_details(context):
    from sinch.domains.sms.models.v1.response.group_response import GroupResponse
    data: GroupResponse = context.response
    assert data.id == '01W4FFL35P4NC4K35SMSGROUP1'
    assert data.name == 'Group master'
    assert data.size == 2
    assert data.created_at == datetime(2024, 6, 6, 8, 59, 22, 156000, tzinfo=timezone.utc)
    assert data.modified_at == datetime(2024, 6, 6, 8, 59, 22, 156000, tzinfo=timezone.utc)
    assert data.child_groups == ['01W4FFL35P4NC4K35SUBGROUP1']




@when('I send a request to list the existing SMS groups')
def step_list_existing_sms_groups(context):
    context.response = context.sms.groups.list()

@when('I send a request to list all the SMS groups')
def step_list_all_sms_groups(context):
    response = context.sms.groups.list(page_size=2)
    groups_list = []
    for group in response.iterator():
        groups_list.append(group)
    context.groups_list = groups_list


@then('the response contains "{count}" SMS groups')
def step_validate_groups_count(context, count):
    expected_count = int(count)
    assert len(context.response.content()) == expected_count, \
        f'Expected {expected_count}, got {len(context.response.content())}'



@when('I iterate manually over the SMS groups pages')
def step_iterate_manually_sms_groups(context):
    context.list_response = context.sms.groups.list(page_size=2)
    context.groups_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.groups_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the SMS groups list contains "{count}" SMS groups')
def step_validate_groups_list_count(context, count):
    expected_count = int(count)
    assert len(context.groups_list) == expected_count, \
        f'Expected {expected_count}, got {len(context.groups_list)}'


@then('the SMS groups iteration result contains the data from "{count}" pages')
def step_validate_groups_pages_count(context, count):
    expected_pages_count = int(count)
    assert context.pages_iteration == expected_pages_count, \
        f'Expected {expected_pages_count} pages, got {context.pages_iteration}'


@when('I send a request to update an SMS group')
def step_update_sms_group(context):
    context.response = context.sms.groups.update(
        group_id='01W4FFL35P4NC4K35SMSGROUP1',
        name='Updated group name',
        add=['+12017771111', '+12017772222'],
        remove=['+12017773333', '+12017774444'],
        add_from_group='01W4FFL35P4NC4K35SMSGROUP2',
        remove_from_group='01W4FFL35P4NC4K35SMSGROUP3',
    )


@then('the response contains the updated SMS group details')
def step_validate_updated_sms_group_details(context):
    from sinch.domains.sms.models.v1.response.group_response import GroupResponse
    data: GroupResponse = context.response
    assert data.id == '01W4FFL35P4NC4K35SMSGROUP1'
    assert data.name == 'Updated group name'
    assert data.size == 6
    assert data.created_at == datetime(2024, 6, 6, 8, 59, 22, 156000, tzinfo=timezone.utc)
    assert data.modified_at == datetime(2024, 6, 6, 9, 19, 58, 147000, tzinfo=timezone.utc)
    assert data.child_groups == ['01W4FFL35P4NC4K35SUBGROUP1']


@when('I send a request to update an SMS group to remove its name')
def step_update_sms_group_remove_name(context):
    context.response = context.sms.groups.update(
        group_id='01W4FFL35P4NC4K35SMSGROUP2',
        name=None,
    )


@then('the response contains the updated SMS group details where the name has been removed')
def step_validate_updated_sms_group_name_removed(context):
    from sinch.domains.sms.models.v1.response.group_response import GroupResponse
    data: GroupResponse = context.response
    assert data.id == '01W4FFL35P4NC4K35SMSGROUP2'
    assert data.name is None
    assert data.size == 5
    assert data.created_at == datetime(2024, 6, 6, 12, 45, 18, 761000, tzinfo=timezone.utc)
    assert data.modified_at == datetime(2024, 6, 6, 13, 12, 5, 137000, tzinfo=timezone.utc)
    assert data.child_groups == []


@when('I send a request to replace an SMS group')
def step_replace_sms_group(context):
    context.response = context.sms.groups.replace(
        group_id='01W4FFL35P4NC4K35SMSGROUP1',
        name='Replacement group',
        members=['+12018881111', '+12018882222', '+12018883333'],
    )


@then('the response contains the replaced SMS group details')
def step_validate_replaced_sms_group_details(context):
    from sinch.domains.sms.models.v1.response.group_response import GroupResponse
    data: GroupResponse = context.response
    assert data.id == '01W4FFL35P4NC4K35SMSGROUP1'
    assert data.name == 'Replacement group'
    assert data.size == 3
    assert data.created_at == datetime(2024, 6, 6, 8, 59, 22, 156000, tzinfo=timezone.utc)
    assert data.modified_at == datetime(2024, 8, 21, 9, 39, 36, 679000, tzinfo=timezone.utc)
    assert data.child_groups == ['01W4FFL35P4NC4K35SUBGROUP1']


@when('I send a request to delete an SMS group')
def step_delete_sms_group(context):
    context.response = context.sms.groups.delete(
        group_id='01W4FFL35P4NC4K35SMSGROUP1',
    )


@then('the delete SMS group response contains no data')
def step_validate_delete_sms_group_response(context):
    assert context.response is None


@when('I send a request to list the members of an SMS group')
def step_list_sms_group_members(context):
    context.response = context.sms.groups.list_members(
        group_id='01W4FFL35P4NC4K35SMSGROUP1',
    )


@then('the response contains the phone numbers of the SMS group')
def step_validate_sms_group_members(context):
    assert context.response.has_next_page is False
    assert context.response.content() == ['12018881111', '12018882222', '12018883333']
