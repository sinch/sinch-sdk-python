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
        # Use service_plan_id for SMS auth, project_id for project auth
        if self._sinch.configuration.authentication_method == "sms_auth":
            path_identifier = self._sinch.configuration.service_plan_id
        else:
            path_identifier = self._sinch.configuration.project_id

        endpoint = ListDeliveryReportsEndpoint(
            project_id=path_identifier,
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
        # Set the authentication method based on configuration
        endpoint.set_authentication_method(self._sinch)

        return SMSPaginator(sinch=self._sinch, endpoint=endpoint)
