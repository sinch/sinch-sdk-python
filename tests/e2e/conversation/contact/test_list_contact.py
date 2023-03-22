from sinch.domains.conversation.models.contact.responses import ListConversationContactsResponse
from sinch.core.pagination import TokenBasedPaginator, AsyncTokenBasedPaginator


def test_list_contacts_sync_limit_1(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list(
        page_size=1
    )
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)
    assert len(list_contacts_response.result.contacts) == 1


async def test_list_contacts_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)
    assert len(list_contacts_response.result.contacts) > 0


def test_list_contacts_using_auto_pagination_sync(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list(
        page_size=1
    )
    page_counter = 1

    for page in list_contacts_response.auto_paging_iter():
        assert isinstance(page, TokenBasedPaginator)
        page_counter += 1

    assert page_counter > 1


async def test_list_contacts_using_auto_pagination_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list(
        page_size=1
    )
    page_counter = 1

    async for page in list_contacts_response.auto_paging_iter():
        assert isinstance(page, AsyncTokenBasedPaginator)
        page_counter += 1

    assert page_counter > 1
