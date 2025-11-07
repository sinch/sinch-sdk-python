from datetime import datetime
from typing import Optional, List, Dict
from sinch.domains.sms.api.v1 import (
    Batches,
    DeliveryReports,
)
from sinch.domains.sms.models.delivery_reports import DeliveryReport
from sinch.domains.sms.models.v1.shared import (
    BinaryRequest,
    MediaRequest,
    MediaBody,
    TextRequest,
)
from sinch.domains.sms.models.v1.types import BatchResponse


class SMS:
    """
    Documentation for Sinch SMS is found at
    https://developers.sinch.com/docs/sms/.
    """

    def __init__(self, sinch):
        self._sinch = sinch

        self.batches = Batches(self._sinch)
        self.delivery_reports = DeliveryReports(self._sinch)

    # ====== High-Level Convenience Methods ======

    # ====== Batches Operations ======
    def send_sms_batch(
        self,
        to: List[str],
        from_: str,
        body: str,
        delivery_report: Optional[DeliveryReport] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        flash_message: Optional[bool] = None,
        max_number_of_message_parts: Optional[int] = None,
        truncate_concat: Optional[bool] = None,
        from_ton: Optional[int] = None,
        from_npi: Optional[int] = None,
        parameters: Optional[Dict[str, Dict[str, str]]] = None,
        **kwargs,
    ) -> BatchResponse:
        return self.batches._send(
            request=TextRequest(
                to=to,
                from_=from_,
                body=body,
                delivery_report=delivery_report,
                send_at=send_at,
                expire_at=expire_at,
                callback_url=callback_url,
                client_reference=client_reference,
                feedback_enabled=feedback_enabled,
                flash_message=flash_message,
                max_number_of_message_parts=max_number_of_message_parts,
                truncate_concat=truncate_concat,
                from_ton=from_ton,
                from_npi=from_npi,
                parameters=parameters,
            ),
            **kwargs,
        )

    def send_binary_batch(
        self,
        to: List[str],
        from_: str,
        body: str,
        udh: str,
        type_: str,
        delivery_report: Optional[DeliveryReport] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        from_ton: Optional[int] = None,
        from_npi: Optional[int] = None,
        **kwargs,
    ):
        return self.batches._send(
            request=BinaryRequest(
                to=to,
                from_=from_,
                body=body,
                udh=udh,
                type_=type_,
                delivery_report=delivery_report,
                send_at=send_at,
                expire_at=expire_at,
                callback_url=callback_url,
                client_reference=client_reference,
                feedback_enabled=feedback_enabled,
                from_ton=from_ton,
                from_npi=from_npi,
            ),
            **kwargs,
        )

    def send_mms_batch(
        self,
        to: List[str],
        from_: str,
        body: MediaBody,
        delivery_report: Optional[DeliveryReport] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        strict_validation: Optional[bool] = None,
        parameters: Optional[Dict[str, Dict[str, str]]] = None,
        **kwargs,
    ) -> BatchResponse:
        return self.batches._send(
            request=MediaRequest(
                to=to,
                from_=from_,
                body=body,
                delivery_report=delivery_report,
                send_at=send_at,
                expire_at=expire_at,
                callback_url=callback_url,
                client_reference=client_reference,
                feedback_enabled=feedback_enabled,
                strict_validation=strict_validation,
                parameters=parameters,
            ),
            **kwargs,
        )
