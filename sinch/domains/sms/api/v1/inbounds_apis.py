




from datetime import datetime
from typing import List, Optional

from sinch.core.pagination import Paginator, SMSPaginator
from sinch.domains.sms.api.v1.base.base_sms import BaseSms
from sinch.domains.sms.api.v1.internal.inbounds_endpoints import (
    GetInboundEndpoint,
    ListInboundsEndpoint,
)
from sinch.domains.sms.models.v1.internal.inbound_id_request import (
    InboundIdRequest,
)
from sinch.domains.sms.models.v1.internal.list_inbounds_request import (
    ListInboundsRequest,
)
from sinch.domains.sms.models.v1.types.inbound_message import InboundMessage


class Inbounds(BaseSms):

    def get(
        self,
        inbound_id: str,
        **kwargs
    ) -> InboundMessage:
        """
        This operation retrieves a specific inbound message using the provided inbound ID.

        :param inbound_id: The inbound ID found when listing inbound messages. (required)
        :type inbound_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: InboundMessage
        :rtype: InboundMessage

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = InboundIdRequest(
            inbound_id=inbound_id,
            **kwargs
        )
        return self._request(GetInboundEndpoint, request_data)
    
    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        to: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        client_reference: Optional[str] = None,
        **kwargs
    ) -> Paginator[InboundMessage]:
        """
        With the list operation,
            you can list all inbound messages that you have received. This operation supports pagination. Inbounds are returned in reverse chronological order.

        :param page: The page number starting from 0. (optional)
        :type page: Optional[int]
        :param page_size: Determines the size of a page (optional)
        :type page_size: Optional[int]
        :param to: Only list messages sent to this destination. Multiple phone numbers formatted as either 
            [E.164](https://community.sinch.com/t5/Glossary/E-164/ta-p/7537) or short codes can be comma separated. 
            (optional)
        :type to: Optional[List[str]]
        :param start_date: Only list messages received at or after this date/time. Formatted as 
            [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`.  Default: Now-24 
            (optional)
        :type start_date: Optional[datetime]
      
            :param end_date: Only list messages received before this date/time. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`. (optional)
        :type end_date: Optional[datetime]
        :param client_reference: Using a client reference in inbound messages requires additional setup on your account. 
            Contact your [account manager](https://dashboard.sinch.com/settings/account-details) to enable this feature.  
            Only list inbound messages that are in response to messages with a previously provided client reference. 
            (optional)
        :type client_reference: Optional[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: Paginator[InboundMessage]
        :rtype: Paginator[InboundMessage]

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        endpoint = ListInboundsEndpoint(
            project_id=self._get_path_identifier(),
            request_data=ListInboundsRequest(
            page=page,
            page_size=page_size,
            to=to,
            start_date=start_date,
            end_date=end_date,
            client_reference=client_reference,
            **kwargs
        )
        )
        
        endpoint.set_authentication_method(self._sinch)

        return SMSPaginator(sinch=self._sinch, endpoint=endpoint)

