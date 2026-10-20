from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.consents.internal.list_audit_records_request import (
    ListAuditRecordsRequest,
)
from sinch.domains.conversation.models.v1.consents.internal.list_consent_identities_request import (
    ListConsentIdentitiesRequest,
)
from sinch.domains.conversation.models.v1.consents.internal.list_consent_identities_response import (
    ListConsentIdentitiesResponse,
)
from sinch.domains.conversation.models.v1.consents.response.audit_records_response import (
    AuditRecordsResponse,
)


class ListConsentIdentitiesEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/apps/{app_id}/consents/{list_type}"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"page_size", "page_token"}

    def __init__(
        self,
        project_id: str,
        request_data: ListConsentIdentitiesRequest,
        response_model=ListConsentIdentitiesResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ListAuditRecordsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}/consents/identities/{identity}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ListAuditRecordsRequest,
        response_model=AuditRecordsResponse,
    ):
        super().__init__(project_id, request_data, response_model)
