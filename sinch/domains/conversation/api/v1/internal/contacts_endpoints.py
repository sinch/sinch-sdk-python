from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.internal.utils import query_params_to_comma_joined_lists
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal.contact_id_request import (
    ContactIdRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.create_contact_request import (
    CreateContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.get_channel_profile_request import (
    GetChannelProfileRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.list_contacts_request import (
    ListContactsRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.list_contacts_response import (
    ListContactsResponse,
)
from sinch.domains.conversation.models.v1.contacts.internal.list_identity_conflicts_request import (
    ListIdentityConflictsRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.list_identity_conflicts_response import (
    ListIdentityConflictsResponse,
)
from sinch.domains.conversation.models.v1.contacts.internal.merge_contact_request import (
    MergeContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.update_contact_request import (
    UpdateContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.contacts.response.get_channel_profile_response import (
    GetChannelProfileResponse,
)


class ListContactsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {
        "channel",
        "external_id",
        "identity",
        "page_size",
        "page_token",
    }

    def __init__(
        self,
        project_id: str,
        request_data: ListContactsRequest,
        response_model=ListContactsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class CreateContactEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: CreateContactRequest,
        response_model=ContactResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetContactEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts/{contact_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ContactIdRequest,
        response_model=ContactResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeleteContactEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts/{contact_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ContactIdRequest):
        super().__init__(project_id, request_data)


class UpdateContactEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts/{contact_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS_EXPLODE_FALSE = {"update_mask"}

    def __init__(
        self,
        project_id: str,
        request_data: UpdateContactRequest,
        response_model=ContactResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def build_query_params(self) -> dict:
        """update_mask lists which fields were set, it isn't a request_data field itself."""
        body_data = self._build_body_data()
        if not body_data:
            return {}
        return query_params_to_comma_joined_lists(
            {"update_mask": list(body_data.keys())}, ["update_mask"]
        )


class MergeContactEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/contacts/{destination_id}:merge"
    )
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: MergeContactRequest,
        response_model=ContactResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetChannelProfileEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/contacts:getChannelProfile"
    )
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: GetChannelProfileRequest,
        response_model=GetChannelProfileResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ListIdentityConflictsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/contacts:identityConflicts"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"page_size", "page_token"}

    def __init__(
        self,
        project_id: str,
        request_data: ListIdentityConflictsRequest,
        response_model=ListIdentityConflictsResponse,
    ):
        super().__init__(project_id, request_data, response_model)
