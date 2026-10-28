from typing import List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.conversation.api.v1.base import BaseConversation
from sinch.domains.conversation.api.v1.internal.capability_endpoints import (
    LookupCapabilityEndpoint,
)
from sinch.domains.conversation.api.v1.internal.utils import (
    build_recipient_dict,
    coerce_recipient,
)
from sinch.domains.conversation.models.v1.capability.internal.lookup_capability_request import (
    LookupCapabilityRequest,
)
from sinch.domains.conversation.models.v1.capability.response.lookup_capability_response import (
    LookupCapabilityResponse,
)
from sinch.domains.conversation.models.v1.messages.types.recipient_dict import (
    ChannelRecipientIdentityDict,
)


class Capability(BaseConversation):
    def lookup(
        self,
        app_id: str,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        request_id: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> LookupCapabilityResponse:
        """
        Capability lookup. This method is asynchronous - it immediately returns the requested
        Capability registration. Capability check is then delivered as a callback to registered
        event destinations with trigger ``CAPABILITY`` for every reachable channel.

        :param app_id: (required) The ID of the app to use for capability lookup.
        :type app_id: str
        :param contact_id: The ID of the recipient contact. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: Channel identities of the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param request_id: (optional) ID for the asynchronous response, will be generated if not set. Currently this field is not used for idempotency.
        :type request_id: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The registered capability lookup.
        :rtype: LookupCapabilityResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        recipient = coerce_recipient(
            build_recipient_dict(
                contact_id=contact_id,
                recipient_identities=recipient_identities,
            )
        )
        request_data = LookupCapabilityRequest(
            app_id=app_id,
            recipient=recipient,
            **strip_unset({"request_id": request_id}),
            **kwargs,
        )
        return self._request(LookupCapabilityEndpoint, request_data)
