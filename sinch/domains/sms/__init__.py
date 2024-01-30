from sinch.core.pagination import IntBasedPaginator
from sinch.core.pagination import AsyncIntBasedPaginator

from sinch.domains.sms.endpoints.batches.send_batch import SendBatchSMSEndpoint
from sinch.domains.sms.endpoints.batches.list_batches import ListSMSBatchesEndpoint
from sinch.domains.sms.endpoints.batches.get_batch import GetSMSEndpoint
from sinch.domains.sms.endpoints.batches.cancel_batch import CancelBatchEndpoint
from sinch.domains.sms.endpoints.batches.update_batch import UpdateBatchSMSEndpoint
from sinch.domains.sms.endpoints.batches.replace_batch import ReplaceBatchSMSEndpoint
from sinch.domains.sms.endpoints.batches.send_delivery_feedback import SendDeliveryReportEndpoint
from sinch.domains.sms.endpoints.batches.send_batch_dry_run import SendBatchSMSDryRunEndpoint

from sinch.domains.sms.endpoints.groups.create_group import CreateSMSGroupEndpoint
from sinch.domains.sms.endpoints.groups.list_groups import ListSMSGroupEndpoint
from sinch.domains.sms.endpoints.groups.delete_group import DeleteSMSGroupEndpoint
from sinch.domains.sms.endpoints.groups.get_group import GetSMSGroupEndpoint
from sinch.domains.sms.endpoints.groups.update_group import UpdateSMSGroupEndpoint
from sinch.domains.sms.endpoints.groups.replace_group import ReplaceSMSGroupEndpoint
from sinch.domains.sms.endpoints.groups.get_phone_numbers_for_group import GetSMSGroupPhoneNumbersEndpoint

from sinch.domains.sms.endpoints.inbounds.list_incoming_messages import ListInboundMessagesEndpoint
from sinch.domains.sms.endpoints.inbounds.get_incoming_message import GetInboundMessagesEndpoint

from sinch.domains.sms.endpoints.delivery_reports.get_delivery_report_for_number import (
    GetDeliveryReportForNumberEndpoint
)
from sinch.domains.sms.endpoints.delivery_reports.get_delivery_report_for_batch import GetDeliveryReportForBatchEndpoint
from sinch.domains.sms.endpoints.delivery_reports.get_all_delivery_reports_for_project import (
    ListDeliveryReportsEndpoint
)

from sinch.domains.sms.models.batches.requests import (
    SendBatchRequest,
    ListBatchesRequest,
    GetBatchRequest,
    BatchDryRunRequest,
    CancelBatchRequest,
    UpdateBatchRequest,
    ReplaceBatchRequest,
    SendDeliveryFeedbackRequest
)

from sinch.domains.sms.models.batches.responses import (
    SendSMSBatchResponse,
    GetSMSBatchResponse,
    CancelSMSBatchResponse,
    SendSMSDeliveryFeedbackResponse,
    ListSMSBatchesResponse,
    UpdateSMSBatchResponse,
    ReplaceSMSBatchResponse,
    SendSMSBatchDryRunResponse
)

from sinch.domains.sms.models.groups.requests import (
    CreateSMSGroupRequest,
    ListSMSGroupRequest,
    DeleteSMSGroupRequest,
    GetSMSGroupRequest,
    GetSMSGroupPhoneNumbersRequest,
    UpdateSMSGroupRequest,
    ReplaceSMSGroupPhoneNumbersRequest
)

from sinch.domains.sms.models.groups.responses import (
    CreateSMSGroupResponse,
    SinchDeleteSMSGroupResponse,
    UpdateSMSGroupResponse,
    SinchListSMSGroupResponse,
    ReplaceSMSGroupResponse,
    GetSMSGroupResponse,
    SinchGetSMSGroupPhoneNumbersResponse
)

from sinch.domains.sms.models.inbounds.requests import (
    ListSMSInboundMessageRequest,
    GetSMSInboundMessageRequest
)

from sinch.domains.sms.models.inbounds.responses import (
    SinchListInboundMessagesResponse,
    GetInboundMessagesResponse
)

from sinch.domains.sms.models.delivery_reports.requests import (
    ListSMSDeliveryReportsRequest,
    GetSMSDeliveryReportForBatchRequest,
    GetSMSDeliveryReportForNumberRequest
)

from sinch.domains.sms.models.delivery_reports.responses import (
    ListSMSDeliveryReportsResponse,
    GetSMSDeliveryReportForBatchResponse,
    GetSMSDeliveryReportForNumberResponse
)


class SMSDeliveryReports:
    def __init__(self, sinch):
        self._sinch = sinch

    def list(
        self,
        page: int = 0,
        start_date: str = None,
        end_date: str = None,
        status: str = None,
        code: str = None,
        page_size: int = None,
        client_reference: str = None
    ) -> ListSMSDeliveryReportsResponse:
        return IntBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListDeliveryReportsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListSMSDeliveryReportsRequest(
                    page=page,
                    page_size=page_size,
                    start_date=start_date,
                    end_date=end_date,
                    status=status,
                    code=code,
                    client_reference=client_reference
                )
            )
        )

    def get_for_batch(
        self,
        batch_id: str,
        type_: str = None,
        code: list = None,
        status: list = None
    ) -> GetSMSDeliveryReportForBatchResponse:
        return self._sinch.configuration.transport.request(
            GetDeliveryReportForBatchEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetSMSDeliveryReportForBatchRequest(
                    batch_id=batch_id,
                    type_=type_,
                    code=code,
                    status=status
                )
            )
        )

    def get_for_number(
        self,
        batch_id: str,
        recipient_number: str
    ) -> GetSMSDeliveryReportForNumberResponse:
        return self._sinch.configuration.transport.request(
            GetDeliveryReportForNumberEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetSMSDeliveryReportForNumberRequest(
                    batch_id=batch_id,
                    recipient_number=recipient_number
                )
            )
        )


class SMSDeliveryReportsWithAsyncPagination(SMSDeliveryReports):
    async def list(
        self,
        page: int = 0,
        start_date: str = None,
        end_date: str = None,
        status: str = None,
        code: str = None,
        page_size: int = None,
        client_reference: str = None
    ) -> ListSMSDeliveryReportsResponse:
        return await AsyncIntBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListDeliveryReportsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListSMSDeliveryReportsRequest(
                    page=page,
                    page_size=page_size,
                    start_date=start_date,
                    end_date=end_date,
                    status=status,
                    code=code,
                    client_reference=client_reference
                )
            )
        )


class SMSInbounds:
    def __init__(self, sinch):
        self._sinch = sinch

    def list(
        self,
        page: int = 0,
        start_date: str = None,
        to: str = None,
        end_date: str = None,
        page_size: int = None,
        client_reference: str = None
    ) -> SinchListInboundMessagesResponse:
        return IntBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListInboundMessagesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListSMSInboundMessageRequest(
                    page=page,
                    page_size=page_size,
                    to=to,
                    end_date=end_date,
                    start_date=start_date,
                    client_reference=client_reference
                )
            )
        )

    def get(self, inbound_id: str) -> GetInboundMessagesResponse:
        return self._sinch.configuration.transport.request(
            GetInboundMessagesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetSMSInboundMessageRequest(
                    inbound_id=inbound_id
                )
            )
        )


class SMSInboundsWithAsyncPagination(SMSInbounds):
    async def list(
        self,
        page: int = 0,
        start_date: str = None,
        to: str = None,
        end_date: str = None,
        page_size: int = None,
        client_reference: str = None
    ) -> SinchListInboundMessagesResponse:
        return await AsyncIntBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListInboundMessagesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListSMSInboundMessageRequest(
                    page=page,
                    page_size=page_size,
                    to=to,
                    end_date=end_date,
                    start_date=start_date,
                    client_reference=client_reference
                )
            )
        )


class SMSBatches:
    def __init__(self, sinch):
        self._sinch = sinch

    def send(
        self,
        body: str,
        delivery_report: str,
        to: list,
        from_: str = None,
        parameters: dict = None,
        type_: str = None,
        send_at: str = None,
        expire_at: str = None,
        callback_url: str = None,
        client_reference: str = None,
        feedback_enabled: bool = None,
        flash_message: bool = None,
        truncate_concat: bool = None,
        max_number_of_message_parts: int = None,
        from_ton: int = None,
        from_npi: int = None
    ) -> SendSMSBatchResponse:
        return self._sinch.configuration.transport.request(
            SendBatchSMSEndpoint(
                sinch=self._sinch,
                request_data=SendBatchRequest(
                    to=to,
                    body=body,
                    from_=from_,
                    delivery_report=delivery_report,
                    feedback_enabled=feedback_enabled,
                    parameters=parameters,
                    type_=type_,
                    send_at=send_at,
                    expire_at=expire_at,
                    callback_url=callback_url,
                    client_reference=client_reference,
                    flash_message=flash_message,
                    truncate_concat=truncate_concat,
                    max_number_of_message_parts=max_number_of_message_parts,
                    from_npi=from_npi,
                    from_ton=from_ton
                )
            )
        )

    def list(
        self,
        page: int = 0,
        page_size: int = None,
        from_s: str = None,
        start_date: str = None,
        end_date: str = None,
        client_reference: str = None
    ) -> ListSMSBatchesResponse:
        return IntBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListSMSBatchesEndpoint(
                sinch=self._sinch,
                request_data=ListBatchesRequest(
                    page=page,
                    page_size=page_size,
                    from_s=from_s,
                    start_date=start_date,
                    end_date=end_date,
                    client_reference=client_reference
                )
            )
        )

    def get(self, batch_id: str) -> GetSMSBatchResponse:
        return self._sinch.configuration.transport.request(
            GetSMSEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetBatchRequest(
                    batch_id=batch_id
                )
            )
        )

    def send_dry_run(
        self,
        to: str,
        body: str,
        per_recipient: bool = None,
        number_of_recipients: int = None,
        from_: str = None,
        type_: str = None,
        udh: str = None,
        delivery_report: str = None,
        send_at: str = None,
        expire_at: str = None,
        callback_url: str = None,
        flash_message: bool = None,
        parameters: dict = None,
        client_reference: str = None,
        max_number_of_message_parts: int = None
    ) -> SendSMSBatchDryRunResponse:
        return self._sinch.configuration.transport.request(
            SendBatchSMSDryRunEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=BatchDryRunRequest(
                    per_recipient=per_recipient,
                    number_of_recipients=number_of_recipients,
                    to=to,
                    body=body,
                    from_=from_,
                    delivery_report=delivery_report,
                    type_=type_,
                    udh=udh,
                    send_at=send_at,
                    expire_at=expire_at,
                    callback_url=callback_url,
                    flash_message=flash_message,
                    parameters=parameters,
                    client_reference=client_reference,
                    max_number_of_message_parts=max_number_of_message_parts
                )
            )
        )

    def cancel(self, batch_id: str) -> CancelSMSBatchResponse:
        return self._sinch.configuration.transport.request(
            CancelBatchEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=CancelBatchRequest(
                    batch_id=batch_id
                )
            )
        )

    def update(
        self,
        batch_id: str,
        to_add: list = None,
        to_remove: list = None,
        from_: str = None,
        body: str = None,
        delivery_report: str = None,
        send_at: str = None,
        expire_at: str = None,
        callback_url: str = None,
    ) -> UpdateSMSBatchResponse:
        return self._sinch.configuration.transport.request(
            UpdateBatchSMSEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateBatchRequest(
                    batch_id=batch_id,
                    to_add=to_add,
                    to_remove=to_remove,
                    from_=from_,
                    body=body,
                    delivery_report=delivery_report,
                    send_at=send_at,
                    expire_at=expire_at,
                    callback_url=callback_url
                )
            )
        )

    def replace(
        self,
        batch_id: str,
        to: str,
        body: str,
        from_: str = None,
        type_: str = None,
        udh: str = None,
        delivery_report: str = None,
        send_at: str = None,
        expire_at: str = None,
        callback_url: str = None,
        flash_message: bool = None,
        parameters: dict = None,
        client_reference: str = None,
        max_number_of_message_parts: int = None
    ) -> ReplaceSMSBatchResponse:
        return self._sinch.configuration.transport.request(
            ReplaceBatchSMSEndpoint(
                sinch=self._sinch,
                request_data=ReplaceBatchRequest(
                    batch_id=batch_id,
                    to=to,
                    body=body,
                    from_=from_,
                    delivery_report=delivery_report,
                    type_=type_,
                    udh=udh,
                    send_at=send_at,
                    expire_at=expire_at,
                    callback_url=callback_url,
                    flash_message=flash_message,
                    client_reference=client_reference,
                    max_number_of_message_parts=max_number_of_message_parts,
                    parameters=parameters
                )
            )
        )

    def send_delivery_feedback(
        self,
        batch_id: str,
        recipients: list
    ) -> SendSMSDeliveryFeedbackResponse:
        return self._sinch.configuration.transport.request(
            SendDeliveryReportEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=SendDeliveryFeedbackRequest(
                    batch_id=batch_id,
                    recipients=recipients
                )
            )
        )


class SMSBatchesWithAsyncPagination(SMSBatches):
    async def list(
        self,
        page: int = 0,
        page_size: int = None,
        from_s: str = None,
        start_date: str = None,
        end_date: str = None,
        client_reference: str = None
    ) -> ListSMSBatchesResponse:
        return await AsyncIntBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListSMSBatchesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListBatchesRequest(
                    page=page,
                    page_size=page_size,
                    from_s=from_s,
                    start_date=start_date,
                    end_date=end_date,
                    client_reference=client_reference
                )
            )
        )


class SMSGroups:
    def __init__(self, sinch):
        self._sinch = sinch

    def create(
        self,
        name: str,
        members: list = None,
        child_groups: list = None,
        auto_update: dict = None
    ) -> CreateSMSGroupResponse:
        return self._sinch.configuration.transport.request(
            CreateSMSGroupEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=CreateSMSGroupRequest(
                    name=name,
                    members=members,
                    child_groups=child_groups,
                    auto_update=auto_update
                )
            )
        )

    def list(
        self,
        page=0,
        page_size=None
    ) -> SinchListSMSGroupResponse:
        return IntBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListSMSGroupEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListSMSGroupRequest(
                    page=page,
                    page_size=page_size
                )
            )
        )

    def delete(
        self,
        group_id: str
    ) -> SinchDeleteSMSGroupResponse:
        return self._sinch.configuration.transport.request(
            DeleteSMSGroupEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=DeleteSMSGroupRequest(
                    group_id=group_id
                )
            )
        )

    def get(
        self,
        group_id: str
    ) -> GetSMSGroupResponse:
        return self._sinch.configuration.transport.request(
            GetSMSGroupEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetSMSGroupRequest(
                    group_id=group_id
                )
            )
        )

    def get_group_phone_numbers(
        self,
        group_id: str
    ) -> SinchGetSMSGroupPhoneNumbersResponse:
        return self._sinch.configuration.transport.request(
            GetSMSGroupPhoneNumbersEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetSMSGroupPhoneNumbersRequest(
                    group_id=group_id
                )
            )
        )

    def update(
        self,
        group_id: str,
        name: str = None,
        add: list = None,
        remove: list = None,
        add_from_group: str = None,
        remove_from_group: str = None,
        auto_update: dict = None
    ) -> UpdateSMSGroupResponse:
        return self._sinch.configuration.transport.request(
            UpdateSMSGroupEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateSMSGroupRequest(
                    group_id=group_id,
                    name=name,
                    add=add,
                    remove=remove,
                    add_from_group=add_from_group,
                    remove_from_group=remove_from_group,
                    auto_update=auto_update
                )
            )
        )

    def replace(
        self,
        group_id: str,
        members: list,
        name: str = None
    ) -> ReplaceSMSGroupResponse:
        return self._sinch.configuration.transport.request(
            ReplaceSMSGroupEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ReplaceSMSGroupPhoneNumbersRequest(
                    group_id=group_id,
                    members=members,
                    name=name
                )
            )
        )


class SMSGroupsWithAsyncPagination(SMSGroups):
    async def list(
        self,
        page=0,
        page_size=None
    ) -> SinchListSMSGroupResponse:
        return await AsyncIntBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListSMSGroupEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListSMSGroupRequest(
                    page=page,
                    page_size=page_size
                )
            )
        )


class SMSBase:
    """
    Documentation for the SMS API: https://developers.sinch.com/docs/sms/
    """
    def __init__(self, sinch):
        self._sinch = sinch


class SMS(SMSBase):
    """
    Synchronous version of the SMS Domain
    """
    __doc__ += SMSBase.__doc__

    def __init__(self, sinch):
        super(SMS, self).__init__(sinch)
        self.groups = SMSGroups(self._sinch)
        self.batches = SMSBatches(self._sinch)
        self.inbounds = SMSInbounds(self._sinch)
        self.delivery_reports = SMSDeliveryReports(self._sinch)


class SMSAsync(SMSBase):
    """
    Asynchronous version of the SMS Domain
    """
    __doc__ += SMSBase.__doc__

    def __init__(self, sinch):
        super(SMSAsync, self).__init__(sinch)
        self.groups = SMSGroupsWithAsyncPagination(self._sinch)
        self.batches = SMSBatchesWithAsyncPagination(self._sinch)
        self.inbounds = SMSInboundsWithAsyncPagination(self._sinch)
        self.delivery_reports = SMSDeliveryReportsWithAsyncPagination(self._sinch)
