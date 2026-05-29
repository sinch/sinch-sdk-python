from typing import List, Optional

from sinch.core.pagination import Paginator, SMSPaginator
from sinch.domains.sms.api.v1.base.base_sms import BaseSms
from sinch.domains.sms.api.v1.internal.groups_endpoints import (
    CreateGroupEndpoint,
    DeleteGroupEndpoint,
    GetGroupEndpoint,
    ListGroupMembersEndpoint,
    ListGroupsEndpoint,
    ReplaceGroupEndpoint,
    UpdateGroupEndpoint,
)
from sinch.domains.sms.models.v1.internal.group_id_request import (
    GroupIdRequest,
)
from sinch.domains.sms.models.v1.internal.group_request import GroupRequest
from sinch.domains.sms.models.v1.internal.list_groups_request import (
    ListGroupsRequest,
)
from sinch.domains.sms.models.v1.internal.replace_group_request import (
    ReplaceGroupRequest,
)
from sinch.domains.sms.models.v1.internal.update_group_request import (
    UpdateGroupRequest,
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

    def get(self, group_id: str, **kwargs) -> GroupResponse:
        """
        This operation retrieves a specific group with the provided group ID.

        :param group_id: ID of a group that you are interested in getting.
        :type group_id: str

        :returns: GroupResponse
        :rtype: GroupResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = GroupIdRequest(group_id=group_id, **kwargs)
        return self._request(GetGroupEndpoint, request_data)

    def replace(
        self,
        group_id: str,
        name: Optional[str] = None,
        members: Optional[List[str]] = None,
        child_groups: Optional[List[str]] = None,
        auto_update: Optional[AutoUpdateDict] = None,
        **kwargs,
    ) -> GroupResponse:
        """
        The replace operation will replace all parameters, including members, of
        an existing group with new values.

        Replacing a group targeted by a batch message scheduled in the future is
        allowed and changes will be reflected when the batch is sent.

        :param group_id: ID of the group to replace.
        :type group_id: str
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
        request_data = ReplaceGroupRequest(
            group_id=group_id,
            name=name,
            members=members,
            child_groups=child_groups,
            auto_update=auto_update,
            **kwargs,
        )
        return self._request(ReplaceGroupEndpoint, request_data)

    def update(
        self,
        group_id: str,
        add: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        name: Optional[str] = None,
        add_from_group: Optional[str] = None,
        remove_from_group: Optional[str] = None,
        auto_update: Optional[AutoUpdateDict] = None,
        **kwargs,
    ) -> GroupResponse:
        """
        With the update group operation, you can add and remove members in an
        existing group as well as rename the group.

        This method encompasses a few ways to update a group:

        1. By using `add` and `remove` arrays containing phone numbers, you control the group
           movements. Any list of valid numbers in E.164 format can be added.
        2. By using the `auto_update` object, your customer can add or remove themselves from groups.
        3. You can also add or remove other groups into this group with `add_from_group` and
           `remove_from_group`.

        Other group update info:

        - The request will not be rejected for duplicate adds or unknown removes.
        - The additions will be done before the deletions. If a phone number is on both lists,
          it will not be part of the resulting group.
        - Updating a group targeted by a batch message scheduled in the future is allowed.
          Changes will be reflected when the batch is sent.

        :param group_id: ID of the group to update.
        :type group_id: str
        :param add: List of phone numbers (MSISDNs) in E.164 format to add to the group. (optional)
        :type add: Optional[List[str]]
        :param remove: List of phone numbers (MSISDNs) in E.164 format to remove from the group. (optional)
        :type remove: Optional[List[str]]
        :param name: Name of the group. Omit to leave the name unchanged; set explicitly to null to
            remove the existing name. (optional)
        :type name: Optional[str]
        :param add_from_group: Copy the members from another group into this group. Must be a valid
            group ID. (optional)
        :type add_from_group: Optional[str]
        :param remove_from_group: Remove the members in a specified group from this group. Must be a
            valid group ID. (optional)
        :type remove_from_group: Optional[str]
        :param auto_update: The auto-update settings for the group. (optional)
        :type auto_update: Optional[AutoUpdateDict]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: GroupResponse
        :rtype: GroupResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = UpdateGroupRequest(
            group_id=group_id,
            add=add,
            remove=remove,
            name=name,
            add_from_group=add_from_group,
            remove_from_group=remove_from_group,
            auto_update=auto_update,
            **kwargs,
        )
        return self._request(UpdateGroupEndpoint, request_data)

    def delete(self, group_id: str) -> None:
        """
        This operation deletes the group with the provided group ID.

        :param group_id: ID of the group to delete.
        :type group_id: str

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = GroupIdRequest(group_id=group_id)
        return self._request(DeleteGroupEndpoint, request_data)

    def list_members(self, group_id: str) -> List[str]:
        """
        This operation retrieves the members of the group with the provided group ID.

        :param group_id: ID of the group whose members are being retrieved.
        :type group_id: str

        :returns: List of phone numbers (MSISDNs) in E.164 format.
        :rtype: List[str]

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = GroupIdRequest(group_id=group_id)
        return self._request(ListGroupMembersEndpoint, request_data)
