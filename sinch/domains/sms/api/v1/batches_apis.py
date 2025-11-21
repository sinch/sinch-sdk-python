from datetime import datetime
from typing import Optional, List, Dict
from pydantic import TypeAdapter, BaseModel
from sinch.core.pagination import Paginator, SMSPaginator
from sinch.domains.sms.models.v1.response.dry_run_response import (
    DryRunResponse,
)
from sinch.domains.sms.models.v1.internal import (
    BatchIdRequest,
    DeliveryFeedbackRequest,
    DryRunRequest,
    ListBatchesRequest,
    ReplaceBatchRequest,
    SendSMSRequest,
    UpdateBatchMessageRequest,
)
from sinch.domains.sms.models.v1.internal.dry_run_request import (
    DryRunTextRequest,
    DryRunBinaryRequest,
    DryRunMediaRequest,
)
from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
    UpdateTextRequestWithBatchId,
    UpdateBinaryRequestWithBatchId,
    UpdateMediaRequestWithBatchId,
)
from sinch.domains.sms.models.v1.internal.replace_batch_request import (
    ReplaceTextRequest,
    ReplaceBinaryRequest,
    ReplaceMediaRequest,
)
from sinch.domains.sms.models.v1.shared import (
    MediaBody,
    TextRequest,
    BinaryRequest,
    MediaRequest,
)
from sinch.domains.sms.models.v1.types import DeliveryReportType
from sinch.domains.sms.api.v1.internal import (
    CancelBatchMessageEndpoint,
    DryRunEndpoint,
    GetBatchMessageEndpoint,
    ListBatchesEndpoint,
    ReplaceBatchEndpoint,
    SendSMSEndpoint,
    DeliveryFeedbackEndpoint,
    UpdateBatchMessageEndpoint,
)
from sinch.domains.sms.api.v1.base import BaseSms
from sinch.domains.sms.models.v1.types import BatchResponse


class Batches(BaseSms):
    def cancel(self, batch_id: str, **kwargs) -> BatchResponse:
        """
        Cancel a batch message

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = BatchIdRequest(batch_id=batch_id, **kwargs)
        return self._request(CancelBatchMessageEndpoint, request_data)

    def dry_run(
        self,
        request: Optional[DryRunRequest] = None,
        per_recipient: Optional[bool] = None,
        number_of_recipients: Optional[int] = None,
        **kwargs,
    ) -> DryRunResponse:
        """
        Dry run

        :param request: The request object. (optional)
        :type request: Optional[DryRunRequest]
        :param per_recipient: Whether to include per recipient details in the response (optional)
        :type per_recipient: Optional[bool]

        :param number_of_recipients: Max number of recipients to include per recipient details for in the response (optional)
        :type number_of_recipients: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: DryRunResponse
        :rtype: DryRunResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        # DryRunRequest is a Union type, so we need to use TypeAdapter to validate
        adapter = TypeAdapter(DryRunRequest)

        # Check if we have any overrides (kwargs or explicit per_recipient/number_of_recipients)
        has_overrides = (
            bool(kwargs)
            or per_recipient is not None
            or number_of_recipients is not None
        )

        if (
            request is not None
            and isinstance(request, BaseModel)
            and not has_overrides
        ):
            request_data = request
        else:
            # Build input data from all sources and merge overrides
            input_data = {}
            if request is not None:
                if isinstance(request, BaseModel):
                    input_data = request.model_dump(exclude_none=True)

            # Merge overrides: kwargs, per_recipient, number_of_recipients
            input_data.update(kwargs)
            if per_recipient is not None:
                input_data["per_recipient"] = per_recipient
            if number_of_recipients is not None:
                input_data["number_of_recipients"] = number_of_recipients

            request_data = adapter.validate_python(input_data)

        return self._request(DryRunEndpoint, request_data)

    def dry_run_sms(
        self,
        to: List[str],
        from_: str,
        body: str,
        per_recipient: Optional[bool] = None,
        number_of_recipients: Optional[int] = None,
        parameters: Optional[Dict[str, Dict[str, str]]] = None,
        delivery_report: Optional[DeliveryReportType] = None,
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
        **kwargs,
    ) -> DryRunResponse:
        """
        Dry run a text SMS batch.

        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: str
        :param per_recipient: Whether to include per recipient details in the response (optional)
        :type per_recipient: Optional[bool]
        :param number_of_recipients: Max number of recipients to include per recipient details for in the response (optional)
        :type number_of_recipients: Optional[int]
        :param parameters: The parameters for the message. (optional)
        :type parameters: Optional[Dict[str, Dict[str, str]]]
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param flash_message: Whether to enable flash message. (optional)
        :type flash_message: Optional[bool]
        :param max_number_of_message_parts: The maximum number of message parts. (optional)
        :type max_number_of_message_parts: Optional[int]
        :param truncate_concat: Whether to truncate the message if it is too long. (optional)
        :type truncate_concat: Optional[bool]
        :param from_ton: The type of number for the sender number. (optional)
        :type from_ton: Optional[int]
        :param from_npi: The number plan indicator for the sender number. (optional)
        :type from_npi: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: DryRunResponse
        :rtype: DryRunResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = DryRunTextRequest(
            to=to,
            from_=from_,
            body=body,
            per_recipient=per_recipient,
            number_of_recipients=number_of_recipients,
            parameters=parameters,
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
            **kwargs,
        )
        return self.dry_run(request=request)

    def dry_run_binary(
        self,
        to: List[str],
        from_: str,
        body: str,
        udh: str,
        per_recipient: Optional[bool] = None,
        number_of_recipients: Optional[int] = None,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        from_ton: Optional[int] = None,
        from_npi: Optional[int] = None,
        **kwargs,
    ) -> DryRunResponse:
        """
        Dry run a binary SMS batch.

        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: str
        :param udh: The user data header. (required)
        :type udh: str
        :param per_recipient: Whether to include per recipient details in the response (optional)
        :type per_recipient: Optional[bool]
        :param number_of_recipients: Max number of recipients to include per recipient details for in the response (optional)
        :type number_of_recipients: Optional[int]
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param from_ton: The type of number for the sender number. (optional)
        :type from_ton: Optional[int]
        :param from_npi: The number plan indicator for the sender number. (optional)
        :type from_npi: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: DryRunResponse
        :rtype: DryRunResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = DryRunBinaryRequest(
            to=to,
            from_=from_,
            body=body,
            udh=udh,
            per_recipient=per_recipient,
            number_of_recipients=number_of_recipients,
            delivery_report=delivery_report,
            send_at=send_at,
            expire_at=expire_at,
            callback_url=callback_url,
            client_reference=client_reference,
            feedback_enabled=feedback_enabled,
            from_ton=from_ton,
            from_npi=from_npi,
            **kwargs,
        )
        return self.dry_run(request=request)

    def dry_run_mms(
        self,
        to: List[str],
        from_: str,
        body: MediaBody,
        per_recipient: Optional[bool] = None,
        number_of_recipients: Optional[int] = None,
        parameters: Optional[Dict[str, Dict[str, str]]] = None,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        strict_validation: Optional[bool] = None,
        **kwargs,
    ) -> DryRunResponse:
        """
        Dry run

        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: MediaBody
        :param per_recipient: Whether to include per recipient details in the response (optional)
        :type per_recipient: Optional[bool]
        :param number_of_recipients: Max number of recipients to include per recipient details for in the response (optional)
        :type number_of_recipients: Optional[int]
        :param parameters: The parameters for the message. (optional)
        :type parameters: Optional[Dict[str, Dict[str, str]]]
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param strict_validation: Whether to enable strict validation. (optional)
        :type strict_validation: Optional[bool]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: DryRunResponse
        :rtype: DryRunResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = DryRunMediaRequest(
            to=to,
            from_=from_,
            body=body,
            per_recipient=per_recipient,
            number_of_recipients=number_of_recipients,
            parameters=parameters,
            delivery_report=delivery_report,
            send_at=send_at,
            expire_at=expire_at,
            callback_url=callback_url,
            client_reference=client_reference,
            feedback_enabled=feedback_enabled,
            strict_validation=strict_validation,
            **kwargs,
        )
        return self.dry_run(request=request)

    def get(self, batch_id: str, **kwargs) -> BatchResponse:
        """
        Get a batch message

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = BatchIdRequest(batch_id=batch_id, **kwargs)
        return self._request(GetBatchMessageEndpoint, request_data)

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        from_: Optional[List[str]] = None,
        client_reference: Optional[str] = None,
        **kwargs,
    ) -> Paginator[BatchResponse]:
        """
        List Batches

        :param page: The page number starting from 0. (optional)
        :type page: Optional[int]
        :param page_size: Determines the size of a page. (optional)
        :type page_size: Optional[int]
        :param start_date: Only list messages received at or after this date/time. Formatted as
            [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`.  Default: Now-24
            (optional)
        :type start_date: Optional[datetime]

        :param end_date: Only list messages received before this date/time. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`. (optional)
        :type end_date: Optional[datetime]

        :param from_: Only list messages sent from this sender number. Multiple originating numbers can be comma separated. Must be phone numbers or short code. (optional)
        :type from_: Optional[List[str]]
        :param client_reference: Client reference to include (optional)
        :type client_reference: Optional[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: Paginator[BatchResponse]
        :rtype: Paginator[BatchResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        endpoint = ListBatchesEndpoint(
            project_id=self._get_path_identifier(),
            request_data=ListBatchesRequest(
                page=page,
                page_size=page_size,
                start_date=start_date,
                end_date=end_date,
                from_=from_,
                client_reference=client_reference,
                **kwargs,
            ),
        )
        endpoint.set_authentication_method(self._sinch)

        return SMSPaginator(sinch=self._sinch, endpoint=endpoint)

    def replace(
        self,
        batch_id: str,
        request: Optional[ReplaceBatchRequest] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        This operation will replace all the parameters of a batch with the provided values. It is the same as cancelling a batch
        and sending a new one instead.

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param request: The request object. (optional)
        :type request: Optional[ReplaceBatchRequest]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        adapter = TypeAdapter(ReplaceBatchRequest)

        input_data = {}
        if request is not None:
            if isinstance(request, BaseModel):
                input_data = request.model_dump(exclude_none=True)

        input_data.update(kwargs)
        input_data["batch_id"] = batch_id

        request_data = adapter.validate_python(input_data)

        return self._request(ReplaceBatchEndpoint, request_data)

    def replace_sms(
        self,
        batch_id: str,
        to: List[str],
        from_: str,
        body: str,
        delivery_report: Optional[DeliveryReportType] = None,
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
        """

        This operation will replace all the parameters of a batch with the provided values. It is the same as cancelling a batch
        and sending a new one instead.

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: str
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param flash_message: Whether to enable flash message. (optional)
        :type flash_message: Optional[bool]
        :param max_number_of_message_parts: The maximum number of message parts. (optional)
        :type max_number_of_message_parts: Optional[int]
        :param truncate_concat: Whether to truncate the message if it is too long. (optional)
        :type truncate_concat: Optional[bool]
        :param from_ton: The type of number for the sender number. (optional)
        :type from_ton: Optional[int]
        :param from_npi: The number plan indicator for the sender number. (optional)
        :type from_npi: Optional[int]
        :param parameters: The parameters for the message. (optional)
        :type parameters: Optional[Dict[str, Dict[str, str]]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        request = ReplaceTextRequest(
            batch_id=batch_id,
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
            **kwargs,
        )
        return self.replace(batch_id=batch_id, request=request)

    def replace_binary(
        self,
        batch_id: str,
        to: List[str],
        from_: str,
        body: str,
        udh: str,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        from_ton: Optional[int] = None,
        from_npi: Optional[int] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        This operation will replace all the parameters of a batch with the provided values.
        It is the same as cancelling a batch and sending a new one instead.

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: str
        :param udh: The user data header. (required)
        :type udh: str
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param from_ton: The type of number for the sender number. (optional)
        :type from_ton: Optional[int]
        :param from_npi: The number plan indicator for the sender number. (optional)
        :type from_npi: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        request = ReplaceBinaryRequest(
            batch_id=batch_id,
            to=to,
            from_=from_,
            body=body,
            udh=udh,
            delivery_report=delivery_report,
            send_at=send_at,
            expire_at=expire_at,
            callback_url=callback_url,
            client_reference=client_reference,
            feedback_enabled=feedback_enabled,
            from_ton=from_ton,
            from_npi=from_npi,
            **kwargs,
        )
        return self.replace(batch_id=batch_id, request=request)

    def replace_mms(
        self,
        batch_id: str,
        to: List[str],
        from_: str,
        body: MediaBody,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        strict_validation: Optional[bool] = None,
        parameters: Optional[Dict[str, Dict[str, str]]] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        This operation will replace all the parameters of a batch with the provided values.
        It is the same as cancelling a batch and sending a new one instead.

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: MediaBody
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param strict_validation: Whether to enable strict validation. (optional)
        :type strict_validation: Optional[bool]
        :param parameters: The parameters for the message. (optional)
        :type parameters: Optional[Dict[str, Dict[str, str]]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        request = ReplaceMediaRequest(
            batch_id=batch_id,
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
            **kwargs,
        )
        return self.replace(batch_id=batch_id, request=request)

    def send(
        self, request: Optional[SendSMSRequest] = None, **kwargs
    ) -> BatchResponse:
        """
        Send a SMS batch.
        :param request: The request object. (optional)
        :type request: Optional[SendSMSRequest]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        # SendSMSRequest is a Union type, so we need to use TypeAdapter to validate
        adapter = TypeAdapter(SendSMSRequest)

        # If request is provided and is already a BaseModel instance, use it directly
        # Otherwise, validate the input (either request dict or kwargs)
        if request is not None and isinstance(request, BaseModel):
            request_data = request
        else:
            # Validate either the request dict or kwargs
            request_data = adapter.validate_python(
                request if request is not None else kwargs
            )

        return self._request(SendSMSEndpoint, request_data)

    def send_sms(
        self,
        to: List[str],
        from_: str,
        body: str,
        delivery_report: Optional[DeliveryReportType] = None,
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
        """
        Send a text SMS batch.

        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: str
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param flash_message: Whether to enable flash message. (optional)
        :type flash_message: Optional[bool]
        :param max_number_of_message_parts: The maximum number of message parts. (optional)
        :type max_number_of_message_parts: Optional[int]
        :param truncate_concat: Whether to truncate the message if it is too long. (optional)
        :type truncate_concat: Optional[bool]
        :param from_ton: The type of number for the sender number. (optional)
        :type from_ton: Optional[int]
        :param from_npi: The number plan indicator for the sender number. (optional)
        :type from_npi: Optional[int]
        :param parameters: The parameters for the message. (optional)
        :type parameters: Optional[Dict[str, Dict[str, str]]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :return: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = TextRequest(
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
            **kwargs,
        )
        return self.send(request=request)

    def send_binary(
        self,
        to: List[str],
        from_: str,
        body: str,
        udh: str,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        from_ton: Optional[int] = None,
        from_npi: Optional[int] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        Send a binary SMS batch.
        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: str
        :param udh: The user data header. (required)
        :type udh: str
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param from_ton: The type of number for the sender number. (optional)
        :type from_ton: Optional[int]
        :param from_npi: The number plan indicator for the sender number. (optional)
        :type from_npi: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :return: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = BinaryRequest(
            to=to,
            from_=from_,
            body=body,
            udh=udh,
            delivery_report=delivery_report,
            send_at=send_at,
            expire_at=expire_at,
            callback_url=callback_url,
            client_reference=client_reference,
            feedback_enabled=feedback_enabled,
            from_ton=from_ton,
            from_npi=from_npi,
            **kwargs,
        )
        return self.send(request=request)

    def send_mms(
        self,
        to: List[str],
        from_: str,
        body: MediaBody,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        strict_validation: Optional[bool] = None,
        parameters: Optional[Dict[str, Dict[str, str]]] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        Send an MMS batch.
        :param to: The list of phone numbers to send the message to. (required)
        :type to: List[str]
        :param from_: The sender phone number. (required)
        :type from_: str
        :param body: The message body. (required)
        :type body: MediaBody
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param strict_validation: Whether to enable strict validation. (optional)
        :type strict_validation: Optional[bool]
        :param parameters: The parameters for the message. (optional)
        :type parameters: Optional[Dict[str, Dict[str, str]]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :return: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = MediaRequest(
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
            **kwargs,
        )
        return self.send(request=request)

    def send_delivery_feedback(
        self, batch_id: str, recipients: List[str], **kwargs
    ) -> None:
        """
        Send delivery feedback for a message

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param recipients: A list of phone numbers (MSISDNs) that have successfully received the message. The key is
            required, however, the value can be an empty array (`[]`) for *a batch*. If the feedback was enabled for *a group*,
            at least one phone number is required. (required)
        :type recipients: List[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request_data = DeliveryFeedbackRequest(
            batch_id=batch_id, recipients=recipients, **kwargs
        )
        return self._request(DeliveryFeedbackEndpoint, request_data)

    def update(
        self,
        batch_id: str,
        request: Optional[UpdateBatchMessageRequest] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        Update a Batch message

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param request: The request object. (optional)
        :type request: Optional[UpdateBatchMessageRequest]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        adapter = TypeAdapter(UpdateBatchMessageRequest)

        input_data = {}
        if request is not None:
            if isinstance(request, BaseModel):
                input_data = request.model_dump(exclude_none=True)
            elif isinstance(request, dict):
                input_data = dict(request)

        input_data.update(kwargs)
        input_data["batch_id"] = batch_id

        request_data = adapter.validate_python(input_data)

        return self._request(UpdateBatchMessageEndpoint, request_data)

    def update_sms(
        self,
        batch_id: str,
        from_: Optional[str] = None,
        to_add: Optional[List[str]] = None,
        to_remove: Optional[List[str]] = None,
        body: Optional[str] = None,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        parameters: Optional[Dict[str, Dict[str, str]]] = None,
        from_ton: Optional[int] = None,
        from_npi: Optional[int] = None,
        max_number_of_message_parts: Optional[int] = None,
        truncate_concat: Optional[bool] = None,
        flash_message: Optional[bool] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        Update a Batch message (SMS)

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param from_: The sender phone number. (optional)
        :type from_: Optional[str]
        :param to_add: The list of phone numbers to add to the batch. (optional)
        :type to_add: Optional[List[str]]
        :param to_remove: The list of phone numbers to remove from the batch. (optional)
        :type to_remove: Optional[List[str]]
        :param body: The message body. (optional)
        :type body: Optional[str]
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param parameters: The parameters for the message. (optional)
        :type parameters: Optional[Dict[str, Dict[str, str]]]
        :param from_ton: The type of number for the sender number. (optional)
        :type from_ton: Optional[int]
        :param from_npi: The number plan indicator for the sender number. (optional)
        :type from_npi: Optional[int]
        :param max_number_of_message_parts: The maximum number of message parts. (optional)
        :type max_number_of_message_parts: Optional[int]
        :param truncate_concat: Whether to truncate the message if it is too long. (optional)
        :type truncate_concat: Optional[bool]
        :param flash_message: Whether to enable flash message. (optional)
        :type flash_message: Optional[bool]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = UpdateTextRequestWithBatchId(
            batch_id=batch_id,
            from_=from_,
            to_add=to_add,
            to_remove=to_remove,
            body=body,
            delivery_report=delivery_report,
            send_at=send_at,
            expire_at=expire_at,
            callback_url=callback_url,
            client_reference=client_reference,
            feedback_enabled=feedback_enabled,
            parameters=parameters,
            from_ton=from_ton,
            from_npi=from_npi,
            max_number_of_message_parts=max_number_of_message_parts,
            truncate_concat=truncate_concat,
            flash_message=flash_message,
            **kwargs,
        )
        return self.update(batch_id=batch_id, request=request)

    def update_binary(
        self,
        batch_id: str,
        udh: str,
        from_: Optional[str] = None,
        to_add: Optional[List[str]] = None,
        to_remove: Optional[List[str]] = None,
        body: Optional[str] = None,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        from_ton: Optional[int] = None,
        from_npi: Optional[int] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        Update a Batch message (Binary)

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param udh: The user data header. (required)
        :type udh: str
        :param from_: The sender phone number. (optional)
        :type from_: Optional[str]
        :param to_add: The list of phone numbers to add to the batch. (optional)
        :type to_add: Optional[List[str]]
        :param to_remove: The list of phone numbers to remove from the batch. (optional)
        :type to_remove: Optional[List[str]]
        :param body: The message body. (optional)
        :type body: Optional[str]
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param from_ton: The type of number for the sender number. (optional)
        :type from_ton: Optional[int]
        :param from_npi: The number plan indicator for the sender number. (optional)
        :type from_npi: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = UpdateBinaryRequestWithBatchId(
            batch_id=batch_id,
            udh=udh,
            from_=from_,
            to_add=to_add,
            to_remove=to_remove,
            body=body,
            delivery_report=delivery_report,
            send_at=send_at,
            expire_at=expire_at,
            callback_url=callback_url,
            client_reference=client_reference,
            feedback_enabled=feedback_enabled,
            from_ton=from_ton,
            from_npi=from_npi,
            **kwargs,
        )
        return self.update(batch_id=batch_id, request=request)

    def update_mms(
        self,
        batch_id: str,
        from_: Optional[str] = None,
        to_add: Optional[List[str]] = None,
        to_remove: Optional[List[str]] = None,
        body: Optional[MediaBody] = None,
        delivery_report: Optional[DeliveryReportType] = None,
        send_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        callback_url: Optional[str] = None,
        client_reference: Optional[str] = None,
        feedback_enabled: Optional[bool] = None,
        parameters: Optional[Dict[str, Dict[str, str]]] = None,
        strict_validation: Optional[bool] = None,
        **kwargs,
    ) -> BatchResponse:
        """
        Update a Batch message (MMS)

        :param batch_id: The batch ID you received from sending a message. (required)
        :type batch_id: str
        :param from_: The sender phone number. (optional)
        :type from_: Optional[str]
        :param to_add: The list of phone numbers to add to the batch. (optional)
        :type to_add: Optional[List[str]]
        :param to_remove: The list of phone numbers to remove from the batch. (optional)
        :type to_remove: Optional[List[str]]
        :param body: The message body. (optional)
        :type body: Optional[MediaBody]
        :param delivery_report: The delivery report type. (optional)
        :type delivery_report: Optional[DeliveryReportType]
        :param send_at: The time to send the message at. (optional)
        :type send_at: Optional[datetime]
        :param expire_at: The time to expire the message at. (optional)
        :type expire_at: Optional[datetime]
        :param callback_url: The callback URL to receive the delivery report. (optional)
        :type callback_url: Optional[str]
        :param client_reference: The client reference to identify the message. (optional)
        :type client_reference: Optional[str]
        :param feedback_enabled: Whether to enable feedback. (optional)
        :type feedback_enabled: Optional[bool]
        :param parameters: The parameters for the message. (optional)
        :type parameters: Optional[Dict[str, Dict[str, str]]]
        :param strict_validation: Whether to enable strict validation. (optional)
        :type strict_validation: Optional[bool]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: BatchResponse
        :rtype: BatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/sms/.
        """
        request = UpdateMediaRequestWithBatchId(
            batch_id=batch_id,
            from_=from_,
            to_add=to_add,
            to_remove=to_remove,
            body=body,
            delivery_report=delivery_report,
            send_at=send_at,
            expire_at=expire_at,
            callback_url=callback_url,
            client_reference=client_reference,
            feedback_enabled=feedback_enabled,
            parameters=parameters,
            strict_validation=strict_validation,
            **kwargs,
        )
        return self.update(batch_id=batch_id, request=request)
