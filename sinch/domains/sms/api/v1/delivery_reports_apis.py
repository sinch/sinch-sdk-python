from datetime import datetime
from typing import List, Optional

from sinch.core.pagination import Paginator, SMSPaginator
from sinch.domains.sms.api.v1.base import BaseSms
from sinch.domains.sms.api.v1.internal import (
    GetBatchDeliveryReportEndpoint,
    GetRecipientDeliveryReportEndpoint,
    ListDeliveryReportsEndpoint,
)
from sinch.domains.sms.models.v1.internal import (
    GetRecipientDeliveryReportRequest,
    ListDeliveryReportsRequest,
    GetBatchDeliveryReportRequest,
)
from sinch.domains.sms.models.v1.response import (
    BatchDeliveryReport,
    RecipientDeliveryReport,
)
from sinch.domains.sms.models.v1.types import (
    DeliveryStatusType,
    DeliveryReceiptStatusCodeType,
)


class DeliveryReports(BaseSms):
    def get(
        self,
        batch_id: str,
        report_type: Optional[str] = None,
        status: Optional[List[DeliveryStatusType]] = None,
        code: Optional[List[DeliveryReceiptStatusCodeType]] = None,
        client_reference: Optional[str] = None,
        **kwargs,
    ) -> BatchDeliveryReport:
        """
        Retrieve a delivery report

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param report_type: The type of delivery report.  - A `summary` will count the number of messages sent per status.  -
            A `full` report give that of a `summary` report but in addition, lists phone numbers. (optional)
        :type report_type: Optional[str]
        :param status: Comma separated list of delivery_report_statuses to include (optional)
        :type status: Optional[List[DeliveryStatusType]]
        :param code: Comma separated list of delivery_receipt_error_codes to include (optional)
        :type code: Optional[List[DeliveryReceiptStatusCodeType]]
        :param client_reference: The client identifier of the batch this delivery report belongs to, if set when submitting batch. (optional)
        :type client_reference: Optional[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchDeliveryReport
        :rtype: BatchDeliveryReport

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = GetBatchDeliveryReportRequest(
            batch_id=batch_id,
            type=report_type,
            status=status,
            code=code,
            client_reference=client_reference,
            **kwargs,
        )
        return self._request(GetBatchDeliveryReportEndpoint, request_data)

    def get_for_number(
        self, batch_id: str, recipient: str, **kwargs
    ) -> RecipientDeliveryReport:
        """
        Retrieve a recipient delivery report

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param recipient: Phone number for which you want to search. (required)
        :type recipient: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: RecipientDeliveryReport
        :rtype: RecipientDeliveryReport

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = GetRecipientDeliveryReportRequest(
            batch_id=batch_id, recipient_msisdn=recipient, **kwargs
        )
        return self._request(GetRecipientDeliveryReportEndpoint, request_data)

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[List[DeliveryStatusType]] = None,
        code: Optional[List[DeliveryReceiptStatusCodeType]] = None,
        client_reference: Optional[str] = None,
        **kwargs,
    ) -> Paginator[RecipientDeliveryReport]:
        """
        Retrieve a list of delivery reports

        :param page: The page number starting from 0. (optional)
        :type page: Optional[int]
        :param page_size: Determines the size of a page. (optional)
        :type page_size: Optional[int]
        :param start_date: Only list messages received at or after this date/time. Default: 24h ago (optional)
        :type start_date: Optional[datetime]
        :param end_date: Only list messages received before this date/time. (optional)
        :type end_date: Optional[datetime]
        :param status: Comma separated list of delivery report statuses to include. (optional)
        :type status: Optional[List[DeliveryStatusType]]
        :param code: Comma separated list of delivery receipt error codes to include. (optional)
        :type code: Optional[List[DeliveryReceiptStatusCodeType]]
        :param client_reference: Client reference to include (optional)
        :type client_reference: Optional[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: Paginator[RecipientDeliveryReport]
        :rtype: Paginator[RecipientDeliveryReport]

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        endpoint = ListDeliveryReportsEndpoint(
            project_id=self._get_path_identifier(),
            request_data=ListDeliveryReportsRequest(
                page=page,
                page_size=page_size,
                start_date=start_date,
                end_date=end_date,
                status=status,
                code=code,
                client_reference=client_reference,
                **kwargs,
            ),
        )
        endpoint.set_authentication_method(self._sinch)

        return SMSPaginator(sinch=self._sinch, endpoint=endpoint)
