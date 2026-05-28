
from typing import List, Optional

from sinch.core.pagination import Paginator, SMSPaginator
from sinch.domains.sms.api.v1.base.base_sms import BaseSms
from sinch.domains.sms.api.v1.internal.groups_endpoints import (
    CreateGroupEndpoint,
    ListGroupsEndpoint,
)
from sinch.domains.sms.models.v1.internal.group_request import GroupRequest
from sinch.domains.sms.models.v1.internal.list_groups_request import (
    ListGroupsRequest,
)
from sinch.domains.sms.models.v1.response.group_response import GroupResponse
from sinch.domains.sms.models.v1.types.auto_update_dict import AutoUpdateDict


class Groups(BaseSms):
    
    def create(
        self,
        name: Optional[str] = None,
        members: Optional[List[str]] = None,
        child_groups: Optional[List[str]] = None,
        auto_update: Optional[AutoUpdateDict] = None,
        **kwargs,
    ) -> GroupResponse:
        """
        This endpoint allows you to create a group of recipients. A new group must be created with a group
        name. This is represented by the `name` field which can be up to 20 characters. In addition, there
        are a number of optional fields:

        - `members` field enables groups to be created with an initial list of contacts.
        - `auto_update` allows customers to auto subscribe to a new group. This contains three fields. The
          `to` field contains the group creator's number. (This number **must be provisioned by contacting
          your account manager**.) The `add` and `remove` fields are objects containing the keywords that
          customers need to text to join or leave a group.

        :param name: Name of the group. Max 20 characters. (optional)
        :type name: Optional[str]
        :param members: Initial list of phone numbers in E.164 format (MSISDNs) for the group. (optional)
        :type members: Optional[List[str]]
        :param child_groups: MSISDNs of child groups to include in this group. If present, this group will
            be auto-populated. Elements must be valid group IDs. (optional)
        :type child_groups: Optional[List[str]]
        :param auto_update: The auto-update settings for the group. (optional)
        :type auto_update: Optional[AutoUpdateDict]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: GroupResponse
        :rtype: GroupResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = GroupRequest(
            name=name,
            members=members,
            child_groups=child_groups,
            auto_update=auto_update,
            **kwargs,
        )
        return self._request(CreateGroupEndpoint, request_data)
    
    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs,
    ) -> Paginator[GroupResponse]:
        """
        With the list operation you can list all groups that you have created.
        This operation supports pagination.

        Groups are returned in reverse chronological order.

        :param page: The page number starting from 0. (optional)
        :type page: Optional[int]
        :param page_size: Determines the size of a page. (optional)
        :type page_size: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: Paginator[GroupResponse]
        :rtype: Paginator[GroupResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        endpoint = ListGroupsEndpoint(
            project_id=self._get_path_identifier(),
            request_data=ListGroupsRequest(
                page=page,
                page_size=page_size,
                **kwargs,
            ),
        )
        endpoint.set_authentication_method(self._sinch)

        return SMSPaginator(sinch=self._sinch, endpoint=endpoint)
        