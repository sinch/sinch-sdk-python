from datetime import datetime
from typing import Optional, List
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
        request_data = BatchIdRequest(batch_id=batch_id, **kwargs)
        return self._request(CancelBatchMessageEndpoint, request_data)

    def dry_run(
        self,
        request: Optional[DryRunRequest] = None,
        per_recipient: Optional[bool] = None,
        number_of_recipients: Optional[int] = None,
        **kwargs,
    ) -> DryRunResponse:
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

    def get(self, batch_id: str, **kwargs) -> BatchResponse:
        request_data = BatchIdRequest(batch_id=batch_id, **kwargs)
        return self._request(GetBatchMessageEndpoint, request_data)

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        var_from: Optional[List[str]] = None,
        client_reference: Optional[str] = None,
        **kwargs,
    ) -> Paginator[BatchResponse]:
        # Use service_plan_id for SMS auth, project_id for project auth
        if self._sinch.configuration.authentication_method == "sms_auth":
            path_identifier = self._sinch.configuration.service_plan_id
        else:
            path_identifier = self._sinch.configuration.project_id

        endpoint = ListBatchesEndpoint(
            project_id=path_identifier,
            request_data=ListBatchesRequest(
                page=page,
                page_size=page_size,
                start_date=start_date,
                end_date=end_date,
                var_from=var_from,
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
        adapter = TypeAdapter(ReplaceBatchRequest)

        input_data = {}
        if request is not None:
            if isinstance(request, BaseModel):
                input_data = request.model_dump(exclude_none=True)

        input_data.update(kwargs)
        input_data["batch_id"] = batch_id

        request_data = adapter.validate_python(input_data)

        return self._request(ReplaceBatchEndpoint, request_data)

    def send(
        self, request: Optional[SendSMSRequest] = None, **kwargs
    ) -> BatchResponse:
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

    def send_delivery_feedback(
        self, batch_id: str, recipients: List[str], **kwargs
    ) -> None:
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
