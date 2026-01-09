# Sinch Python SDK Migration Guide

## 2.0.0

This release removes legacy SDK support.

This guide lists all removed classes and interfaces from V1 and how to migrate to their V2 equivalents.

## Client Initialization

### Overview

In V2, region parameters are required for domain-specific APIs (SMS and Conversation). These parameters must be set explicitly when initializing `SinchClient`, otherwise API calls will fail at runtime. The parameters are exposed directly on `SinchClient` to ensure they are provided.

### SMS Region

**In V1:**
```python
from sinch import SinchClient

# Using Project auth
sinch_client = SinchClient(
    project_id="your-project-id",
    key_id="your-key-id",
    key_secret="your-key-secret",
)
sinch_client.configuration.sms_region = "eu"

# Or using SMS token auth
token_client = SinchClient(
    service_plan_id='your-service-plan-id',
    sms_api_token='your-sms-api-token'
)
token_client.configuration.sms_region_with_service_plan_id = "eu"
```

**In V2:**
- The `sms_region` no longer defaults to `us`. Set it explicitly before using the SMS API, otherwise calls will fail at runtime. The parameter is now exposed on `SinchClient` (not just the configuration object) to ensure the region is provided. Note that `sms_region` is only required when using the SMS API endpoints.

```python
from sinch import SinchClient

# Using Project auth
sinch_client = SinchClient(
    project_id="your-project-id",
    key_id="your-key-id",
    key_secret="your-key-secret",
    sms_region="eu",
)

# Or using SMS token auth
token_client = SinchClient(
    service_plan_id="your-service-plan-id",
    sms_api_token="your-sms-api-token",
    sms_region="us",
)

# Note: The code is backward compatible. The sms_region can still be set through the configuration object,
# but you must ensure this setting is done BEFORE any SMS API call:
sinch_client.configuration.sms_region = "eu"
```

### Conversation Region

**In V1:**
```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="your-project-id",
    key_id="your-key-id",
    key_secret="your-key-secret",
)

sinch_client.configuration.conversation_region = "eu"
```

**In V2:**
- The `conversation_region` no longer defaults to `eu`. This parameter is required now when using the Conversation API endpoints. Set it explicitly when initializing `SinchClient`, otherwise calls will fail at runtime. The parameter is exposed on `SinchClient` to ensure the region is provided.

```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="your-project-id",
    key_id="your-key-id",
    key_secret="your-key-secret",
    conversation_region="eu",
)

# Note: The conversation_region can also be set through the configuration object,
# but you must ensure this setting is done BEFORE any Conversation API call:
sinch_client.configuration.conversation_region = "eu"
```

### [`SMS`](https://github.com/sinch/sinch-sdk-python/tree/main/sinch/domains/sms)

#### Replacement models

##### Batches

| Old class | New class |
|-----------|-----------|
| `sinch.domains.sms.models.batches.requests.BatchRequest` | [`sinch.domains.sms.models.v1.shared.TextRequest`](sinch/domains/sms/models/v1/shared/text_request.py), [`sinch.domains.sms.models.v1.shared.BinaryRequest`](sinch/domains/sms/models/v1/shared/binary_request.py), or [`sinch.domains.sms.models.v1.shared.MediaRequest`](sinch/domains/sms/models/v1/shared/media_request.py) |
| `sinch.domains.sms.models.batches.requests.SendBatchRequest` | [`sinch.domains.sms.models.v1.shared.TextRequest`](sinch/domains/sms/models/v1/shared/text_request.py), [`sinch.domains.sms.models.v1.shared.BinaryRequest`](sinch/domains/sms/models/v1/shared/binary_request.py), or [`sinch.domains.sms.models.v1.shared.MediaRequest`](sinch/domains/sms/models/v1/shared/media_request.py) |
| `sinch.domains.sms.models.batches.requests.ListBatchesRequest` | [`sinch.domains.sms.models.v1.internal.ListBatchesRequest`](sinch/domains/sms/models/v1/internal/list_batches_request.py) |
| `sinch.domains.sms.models.batches.requests.GetBatchRequest` | [`sinch.domains.sms.models.v1.internal.BatchIdRequest`](sinch/domains/sms/models/v1/internal/batch_id_request.py) |
| `sinch.domains.sms.models.batches.requests.CancelBatchRequest` | [`sinch.domains.sms.models.v1.internal.BatchIdRequest`](sinch/domains/sms/models/v1/internal/batch_id_request.py) |
| `sinch.domains.sms.models.batches.requests.BatchDryRunRequest` | [`sinch.domains.sms.models.v1.internal.DryRunRequest`](sinch/domains/sms/models/v1/internal/dry_run_request.py) (Union of [`DryRunTextRequest`](sinch/domains/sms/models/v1/internal/dry_run_request.py), [`DryRunBinaryRequest`](sinch/domains/sms/models/v1/internal/dry_run_request.py), [`DryRunMediaRequest`](sinch/domains/sms/models/v1/internal/dry_run_request.py)) |
| `sinch.domains.sms.models.batches.requests.UpdateBatchRequest` | [`sinch.domains.sms.models.v1.internal.UpdateBatchMessageRequest`](sinch/domains/sms/models/v1/internal/update_batch_message_request.py) (Union of [`UpdateTextRequestWithBatchId`](sinch/domains/sms/models/v1/internal/update_batch_message_request.py), [`UpdateBinaryRequestWithBatchId`](sinch/domains/sms/models/v1/internal/update_batch_message_request.py), [`UpdateMediaRequestWithBatchId`](sinch/domains/sms/models/v1/internal/update_batch_message_request.py)) |
| `sinch.domains.sms.models.batches.requests.ReplaceBatchRequest` | [`sinch.domains.sms.models.v1.internal.ReplaceBatchRequest`](sinch/domains/sms/models/v1/internal/replace_batch_request.py) (Union of [`ReplaceTextRequest`](sinch/domains/sms/models/v1/internal/replace_batch_request.py), [`ReplaceBinaryRequest`](sinch/domains/sms/models/v1/internal/replace_batch_request.py), [`ReplaceMediaRequest`](sinch/domains/sms/models/v1/internal/replace_batch_request.py)) |
| `sinch.domains.sms.models.batches.requests.SendDeliveryFeedbackRequest` | [`sinch.domains.sms.models.v1.internal.DeliveryFeedbackRequest`](sinch/domains/sms/models/v1/internal/delivery_feedback_request.py) |
| `sinch.domains.sms.models.batches.responses.SendSMSBatchResponse` | [`sinch.domains.sms.models.v1.types.BatchResponse`](sinch/domains/sms/models/v1/types/batch_response.py) (Union of [`TextResponse`](sinch/domains/sms/models/v1/shared/text_response.py), [`BinaryResponse`](sinch/domains/sms/models/v1/shared/binary_response.py), [`MediaResponse`](sinch/domains/sms/models/v1/shared/media_response.py)) |
| `sinch.domains.sms.models.batches.responses.ReplaceSMSBatchResponse` | [`sinch.domains.sms.models.v1.types.BatchResponse`](sinch/domains/sms/models/v1/types/batch_response.py) |
| `sinch.domains.sms.models.batches.responses.ListSMSBatchesResponse` | [`sinch.domains.sms.models.v1.response.ListBatchesResponse`](sinch/domains/sms/models/v1/response/list_batches_response.py) |
| `sinch.domains.sms.models.batches.responses.GetSMSBatchResponse` | [`sinch.domains.sms.models.v1.types.BatchResponse`](sinch/domains/sms/models/v1/types/batch_response.py) |
| `sinch.domains.sms.models.batches.responses.CancelSMSBatchResponse` | [`sinch.domains.sms.models.v1.types.BatchResponse`](sinch/domains/sms/models/v1/types/batch_response.py) |
| `sinch.domains.sms.models.batches.responses.SendSMSBatchDryRunResponse` | [`sinch.domains.sms.models.v1.response.DryRunResponse`](sinch/domains/sms/models/v1/response/dry_run_response.py) |
| `sinch.domains.sms.models.batches.responses.UpdateSMSBatchResponse` | [`sinch.domains.sms.models.v1.types.BatchResponse`](sinch/domains/sms/models/v1/types/batch_response.py) |
| `sinch.domains.sms.models.batches.responses.SendSMSDeliveryFeedbackResponse` | `None` (The method returns an empty 202 HTTP response) |

##### Delivery Reports

| Old class | New class |
|-----------|-----------|
| `sinch.domains.sms.models.delivery_reports.requests.ListSMSDeliveryReportsRequest` | [`sinch.domains.sms.models.v1.internal.ListDeliveryReportsRequest`](sinch/domains/sms/models/v1/internal/list_delivery_reports_request.py) |
| `sinch.domains.sms.models.delivery_reports.requests.GetSMSDeliveryReportForBatchRequest` | [`sinch.domains.sms.models.v1.internal.GetBatchDeliveryReportRequest`](sinch/domains/sms/models/v1/internal/get_batch_delivery_report_request.py) |
| `sinch.domains.sms.models.delivery_reports.requests.GetSMSDeliveryReportForNumberRequest` | [`sinch.domains.sms.models.v1.internal.GetRecipientDeliveryReportRequest`](sinch/domains/sms/models/v1/internal/get_recipient_delivery_report_request.py) |
| `sinch.domains.sms.models.delivery_reports.responses.ListSMSDeliveryReportsResponse` | [`sinch.domains.sms.models.v1.internal.ListDeliveryReportsResponse`](sinch/domains/sms/models/v1/internal/list_delivery_reports_response.py) |
| `sinch.domains.sms.models.delivery_reports.responses.GetSMSDeliveryReportForBatchResponse` | [`sinch.domains.sms.models.v1.response.BatchDeliveryReport`](sinch/domains/sms/models/v1/response/batch_delivery_report.py) |
| `sinch.domains.sms.models.delivery_reports.responses.GetSMSDeliveryReportForNumberResponse` | [`sinch.domains.sms.models.v1.response.RecipientDeliveryReport`](sinch/domains/sms/models/v1/response/recipient_delivery_report.py) |

#### Replacement APIs

The SMS domain API access remains the same: `sinch.sms.batches` and `sinch.sms.delivery_reports`. However, the underlying models and method signatures have changed.
Note that `sinch.sms.groups` and `sinch.sms.inbounds` are not supported yet and will be available in future minor versions.

##### Batches API

| Old method | New method in `sms.batches` |
|------------|----------------------------|
| `send()` with `SendBatchRequest` | Use convenience methods: `send_sms()`, `send_binary()`, `send_mms()`<br>Or `send()` with `SendSMSRequest` (Union of `TextRequest`, `BinaryRequest`, `MediaRequest`) |
| `list()` with `ListBatchesRequest` | `list()` with individual parameters: `page`, `page_size`, `start_date`, `end_date`, `from_`, `client_reference` |
| `get()` with `GetBatchRequest` | `get()` with `batch_id: str` parameter |
| `send_dry_run()` with `BatchDryRunRequest` | Use convenience methods: `dry_run_sms()`, `dry_run_binary()`, `dry_run_mms()`<br>Or `dry_run()` with `DryRunRequest` (Union of `DryRunTextRequest`, `DryRunBinaryRequest`, `DryRunMediaRequest`) |
| `update()` with `UpdateBatchRequest` | Use convenience methods: `update_sms()`, `update_binary()`, `update_mms()`<br>Or `update()` with `UpdateBatchMessageRequest` (Union of `UpdateTextRequestWithBatchId`, `UpdateBinaryRequestWithBatchId`, `UpdateMediaRequestWithBatchId`) |
| `replace()` with `ReplaceBatchRequest` | Use convenience methods: `replace_sms()`, `replace_binary()`, `replace_mms()`<br>Or `replace()` with `ReplaceBatchRequest` (Union of `ReplaceTextRequest`, `ReplaceBinaryRequest`, `ReplaceMediaRequest`) |

<br>

##### Delivery Reports API

| Old method | New method in `sms.delivery_reports` |
|------------|-------------------------------------|
| `list()` with `ListSMSDeliveryReportsRequest` | `list()` the parameters `start_date` and `end_date` now accepts both `str` and `datetime`  |
| `get_for_batch()` with `GetSMSDeliveryReportForBatchRequest` | `get()` with `batch_id: str` and optional parameters: `report_type`, `status`, `code`, `client_reference` |
| `get_for_number()` with `GetSMSDeliveryReportForNumberRequest` | `get_for_number()` with `batch_id: str` and `recipient: str` parameters |
