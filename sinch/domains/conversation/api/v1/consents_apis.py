from typing import Optional

from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.domains.conversation.api.v1.base import BaseConversation
from sinch.domains.conversation.api.v1.internal.consents_endpoints import (
    ListAuditRecordsEndpoint,
    ListConsentIdentitiesEndpoint,
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
from sinch.domains.conversation.models.v1.consents.response.consent_identity_response import (
    ConsentIdentityResponse,
)
from sinch.domains.conversation.models.v1.consents.types.consents_list_type import (
    ConsentsListType,
)


class Consents(BaseConversation):
    def list_identities(
        self,
        app_id: str,
        list_type: ConsentsListType,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        **kwargs,
    ) -> Paginator[ListConsentIdentitiesResponse, ConsentIdentityResponse]:
        """
        Get all identities contained within a consent list for a given project id, app id,
        and list type.

        :param app_id: (required) The unique ID of the app.
        :type app_id: str
        :param list_type: (required) The consent list type. One of ``OPT_OUT_ALL``,
            ``OPT_OUT_MARKETING`` and ``OPT_OUT_NOTIFICATION``.
        :type list_type: ConsentsListType
        :param page_size: (optional) The maximum number of records to fetch. The server
            default is 10 and the maximum is 50.
        :type page_size: Optional[int]
        :param page_token: (optional) A page token, received from a previous call. Provide
            this to retrieve a subsequent page.
        :type page_token: Optional[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: A paginator for iterating through the identities of the consent list.
        :rtype: Paginator[ListConsentIdentitiesResponse, ConsentIdentityResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListConsentIdentitiesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConsentIdentitiesRequest(
                    app_id=app_id,
                    list_type=list_type,
                    page_size=page_size,
                    page_token=page_token,
                    **kwargs,
                ),
            ),
        )

    def list_audit_records(
        self, app_id: str, identity: str, **kwargs
    ) -> AuditRecordsResponse:
        """
        Get all audit records associated with the given identity from the consent lists within
        the specified project and app.

        :param app_id: (required) The unique ID of the app.
        :type app_id: str
        :param identity: (required) An identity to use on Consent audit records queries.
        :type identity: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The identity and its audit records.
        :rtype: AuditRecordsResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = ListAuditRecordsRequest(
            app_id=app_id, identity=identity, **kwargs
        )
        return self._request(ListAuditRecordsEndpoint, request_data)
