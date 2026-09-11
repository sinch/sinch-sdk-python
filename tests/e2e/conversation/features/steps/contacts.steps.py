from behave import given, when, then
from sinch.domains.conversation.api.v1.contacts_apis import Contacts


@given('the Conversation service "Contacts" is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.contacts, Contacts), 'Contacts service is not available'
    context.contacts = context.sinch.conversation.contacts


@when('I send a request to create a contact')
def step_create_contact(context):
    context.create_contact_response = context.contacts.create(
        channel_identities=[{'channel': 'SMS', 'identity': '+12015555555'}],
        language='EN_US',
        display_name='Marty McFly',
        email='time.traveler@delorean.com',
    )


@then('the contact is created')
def step_validate_create_contact(context):
    contact = context.create_contact_response
    assert contact is not None, 'Create contact response should not be None'
    assert contact.id == '01W4FFL35P4NC4K35CONTACT001', (
        f'Expected contact.id to be "01W4FFL35P4NC4K35CONTACT001", got "{contact.id}"'
    )
    assert contact.display_name == 'Marty McFly', (
        f'Expected contact.display_name to be "Marty McFly", got "{contact.display_name}"'
    )
    assert contact.email == 'time.traveler@delorean.com', (
        f'Expected contact.email to be "time.traveler@delorean.com", got "{contact.email}"'
    )
    assert contact.language == 'EN_US', (
        f'Expected contact.language to be "EN_US", got "{contact.language}"'
    )
    assert contact.channel_identities[0].channel == 'SMS', (
        f'Expected first channel to be "SMS", got "{contact.channel_identities[0].channel}"'
    )
    assert contact.channel_identities[0].identity == '12015555555', (
        f'Expected first identity to be "12015555555", got "{contact.channel_identities[0].identity}"'
    )


@when('I send a request to list the existing contacts')
def step_list_contacts_page(context):
    context.list_response = context.contacts.list(page_size=2)


@then('the response contains "{count}" contacts')
def step_validate_contacts_page_count(context, count):
    expected_contacts_count = int(count)
    contacts_page = context.list_response.content()
    assert len(contacts_page) == expected_contacts_count, (
        f'Expected {expected_contacts_count} contacts, got {len(contacts_page)}'
    )


@when('I send a request to list all the contacts')
def step_list_all_contacts(context):
    response = context.contacts.list(page_size=2)
    context.contacts_list = list(response.iterator())


@then('the contacts list contains "{count}" contacts')
def step_validate_total_contacts_count(context, count):
    expected_contacts_count = int(count)
    assert len(context.contacts_list) == expected_contacts_count, (
        f'Expected {expected_contacts_count} contacts, got {len(context.contacts_list)}'
    )


@when('I iterate manually over the contacts pages')
def step_iterate_contacts_pages(context):
    context.list_response = context.contacts.list(page_size=2)

    context.contacts_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.contacts_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the contacts iteration result contains the data from "{count}" pages')
def step_validate_contacts_page_iteration_count(context, count):
    expected_pages_count = int(count)
    assert context.pages_iteration == expected_pages_count, (
        f'Expected {expected_pages_count} pages, got {context.pages_iteration}'
    )


@when('I send a request to retrieve a contact')
def step_retrieve_contact(context):
    context.contact = context.contacts.get(
        contact_id='01W4FFL35P4NC4K35CONTACT001'
    )


@then('the response contains the contact details')
def step_validate_contact_details(context):
    contact = context.contact
    assert contact is not None, 'Contact should not be None'
    assert contact.id == '01W4FFL35P4NC4K35CONTACT001', (
        f'Expected contact.id to be "01W4FFL35P4NC4K35CONTACT001", got "{contact.id}"'
    )
    assert contact.display_name == 'Marty McFly', (
        f'Expected contact.display_name to be "Marty McFly", got "{contact.display_name}"'
    )
    assert contact.email == 'time.traveler@delorean.com', (
        f'Expected contact.email to be "time.traveler@delorean.com", got "{contact.email}"'
    )
    assert contact.language == 'EN_US', (
        f'Expected contact.language to be "EN_US", got "{contact.language}"'
    )
    assert contact.channel_identities[0].channel == 'SMS', (
        f'Expected first channel to be "SMS", got "{contact.channel_identities[0].channel}"'
    )


@when('I send a request to update a contact')
def step_update_contact(context):
    context.update_contact_response = context.contacts.update(
        contact_id='01W4FFL35P4NC4K35CONTACT001',
        channel_identities=[
            {
                'channel': 'MESSENGER',
                'identity': '7968425018576406',
                'app_id': '01W4FFL35P4NC4K35CONVAPP001',
            },
            {'channel': 'SMS', 'identity': '12015555555'},
        ],
        channel_priority=['MESSENGER'],
    )


@then('the response contains the contact details with updated data')
def step_validate_update_contact(context):
    contact = context.update_contact_response
    assert contact is not None, 'Update contact response should not be None'
    assert contact.id == '01W4FFL35P4NC4K35CONTACT001', (
        f'Expected contact.id to be "01W4FFL35P4NC4K35CONTACT001", got "{contact.id}"'
    )
    assert contact.channel_priority == ['MESSENGER'], (
        f'Expected channel_priority to be ["MESSENGER"], got {contact.channel_priority}'
    )
    assert len(contact.channel_identities) == 2, (
        f'Expected 2 channel identities, got {len(contact.channel_identities)}'
    )
    assert contact.channel_identities[0].channel == 'MESSENGER', (
        f'Expected first channel to be "MESSENGER", got "{contact.channel_identities[0].channel}"'
    )
    assert contact.channel_identities[0].identity == '7968425018576406', (
        f'Expected first identity to be "7968425018576406", got "{contact.channel_identities[0].identity}"'
    )
    assert contact.channel_identities[0].app_id == '01W4FFL35P4NC4K35CONVAPP001', (
        f'Expected first app_id to be "01W4FFL35P4NC4K35CONVAPP001", got "{contact.channel_identities[0].app_id}"'
    )
    assert contact.channel_identities[1].channel == 'SMS', (
        f'Expected second channel to be "SMS", got "{contact.channel_identities[1].channel}"'
    )


@when('I send a request to delete a contact')
def step_delete_contact(context):
    context.delete_contact_response = context.contacts.delete(
        contact_id='01W4FFL35P4NC4K35CONTACT001'
    )


@then('the delete contact response contains no data')
def step_validate_delete_contact_response(context):
    assert context.delete_contact_response is None, 'Delete contact response should be None'


@when('I send a request to merge a source contact to a destination contact')
def step_merge_contacts(context):
    context.merge_contact_response = context.contacts.merge_contact(
        destination_id='01W4FFL35P4NC4K35CONTACT002',
        source_id='01W4FFL35P4NC4K35CONTACT001',
    )


@then('the response contains data from the destination contact and from the source contact')
def step_validate_merge_contacts(context):
    contact = context.merge_contact_response
    assert contact is not None, 'Merge contact response should not be None'
    assert contact.id == '01W4FFL35P4NC4K35CONTACT002', (
        f'Expected contact.id to be "01W4FFL35P4NC4K35CONTACT002", got "{contact.id}"'
    )
    assert contact.display_name == 'Pika pika', (
        f'Expected contact.display_name to be "Pika pika", got "{contact.display_name}"'
    )
    assert contact.channel_priority == ['MMS', 'MESSENGER'], (
        f'Expected channel_priority to be ["MMS", "MESSENGER"], got {contact.channel_priority}'
    )
    assert len(contact.channel_identities) == 3, (
        f'Expected 3 channel identities, got {len(contact.channel_identities)}'
    )


@when('I send a request to get the channel profile of a contact ID')
def step_get_channel_profile(context):
    context.channel_profile_response = context.contacts.get_channel_profile_by_contact_id(
        app_id='01W4FFL35P4NC4K35CONVAPP001',
        channel='MESSENGER',
        contact_id='01W4FFL35P4NC4K35CONTACT001',
    )


@then('the response contains the profile of the contact on the requested channel')
def step_validate_channel_profile(context):
    profile = context.channel_profile_response
    assert profile is not None, 'Channel profile response should not be None'
    assert profile.profile_name == 'Marty McFly FB', (
        f'Expected profile_name to be "Marty McFly FB", got "{profile.profile_name}"'
    )


@when('I send a request to list the existing identity conflicts')
def step_list_identity_conflicts_page(context):
    context.identity_conflicts_response = context.contacts.list_identity_conflicts(
        page_size=2
    )


@then('the response contains "{count}" identity conflicts')
def step_validate_identity_conflicts_page_count(context, count):
    expected_count = int(count)
    conflicts_page = context.identity_conflicts_response.content()
    assert len(conflicts_page) == expected_count, (
        f'Expected {expected_count} identity conflicts, got {len(conflicts_page)}'
    )


@when('I send a request to list all the identity conflicts')
def step_list_all_identity_conflicts(context):
    response = context.contacts.list_identity_conflicts(page_size=2)
    context.identity_conflicts_list = list(response.iterator())


@then('the identity conflicts list contains "{count}" identity conflicts')
def step_validate_total_identity_conflicts_count(context, count):
    expected_count = int(count)
    assert len(context.identity_conflicts_list) == expected_count, (
        f'Expected {expected_count} identity conflicts, got {len(context.identity_conflicts_list)}'
    )


@when('I iterate manually over the identity conflicts pages')
def step_iterate_identity_conflicts_pages(context):
    context.identity_conflicts_response = context.contacts.list_identity_conflicts(
        page_size=2
    )

    context.identity_conflicts_list = []
    context.identity_conflicts_pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.identity_conflicts_list.extend(
            context.identity_conflicts_response.content()
        )
        context.identity_conflicts_pages_iteration += 1
        if context.identity_conflicts_response.has_next_page:
            context.identity_conflicts_response = (
                context.identity_conflicts_response.next_page()
            )
        else:
            reached_end_of_pages = True


@then('the identity conflicts iteration result contains the data from "{count}" pages')
def step_validate_identity_conflicts_page_iteration_count(context, count):
    expected_pages_count = int(count)
    assert context.identity_conflicts_pages_iteration == expected_pages_count, (
        f'Expected {expected_pages_count} pages, got {context.identity_conflicts_pages_iteration}'
    )
