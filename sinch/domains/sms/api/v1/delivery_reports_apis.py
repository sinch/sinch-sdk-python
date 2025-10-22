from datetime import datetime
from typing import List, Optional

from sinch.core.pagination import Paginator, SMSPaginator
from sinch.domains.sms.api.v1.base import BaseSms
from sinch.domains.sms.api.v1.internal import (
    GetDeliveryReportByBatchIdEndpoint,
    GetDeliveryReportByPhoneNumberEndpoint,
    ListDeliveryReportsEndpoint,
)
from sinch.domains.sms.models.v1.internal import (
    GetDeliveryReportByPhoneNumberRequest,
    ListDeliveryReportsRequest,
    GetDeliveryReportsByBatchIdRequest,
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
        request_data = GetDeliveryReportsByBatchIdRequest(
            batch_id=batch_id,
            type=report_type,
            status=status,
            code=code,
            client_reference=client_reference,
            **kwargs,
        )
        return self._request(GetDeliveryReportByBatchIdEndpoint, request_data)

    def get_for_number(
        self, batch_id: str, recipient: str, **kwargs
    ) -> RecipientDeliveryReport:
        request_data = GetDeliveryReportByPhoneNumberRequest(
            batch_id=batch_id, recipient_msisdn=recipient, **kwargs
        )
        return self._request(
            GetDeliveryReportByPhoneNumberEndpoint, request_data
        )

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
        return SMSPaginator(
            sinch=self._sinch,
            endpoint=ListDeliveryReportsEndpoint(
                project_id=self._sinch.configuration.project_id,
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
            ),
        )
