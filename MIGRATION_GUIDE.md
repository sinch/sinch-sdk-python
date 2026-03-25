# Sinch Python SDK Migration Guide

## 2.0.0

This release removes legacy SDK support.

This guide lists all removed classes and interfaces from V1 and how to migrate to their V2 equivalents.

> **Note:** Voice and Verification are not yet covered by the new V2 APIs. Support will be added in future releases.

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

### [`Conversation`](https://github.com/sinch/sinch-sdk-python/tree/main/sinch/domains/conversation)

#### Replacement models

##### Messages (send, get, delete, list)

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.message.requests.SendConversationMessageRequest` | `send()`: pass `app_id`, `message` (dict or [`SendMessageRequestBodyDict`](sinch/domains/conversation/models/v1/messages/types/send_message_request_body_dict.py)), and either `contact_id` or `recipient_identities`. Internally uses [`SendMessageRequest`](sinch/domains/conversation/models/v1/messages/internal/request/send_message_request.py), [`SendMessageRequestBody`](sinch/domains/conversation/models/v1/messages/internal/request/send_message_request_body.py). For typed payloads use `send_text_message()`, `send_card_message()`, etc.
| `sinch.domains.conversation.models.message.responses.SendConversationMessageResponse` | [`SendMessageResponse`](sinch/domains/conversation/models/v1/messages/response/send_message_response.py) (`message_id`, optional `accepted_time` as `datetime`) |
| `sinch.domains.conversation.models.message.requests.GetConversationMessageRequest` | `get(message_id, messages_source=None, **kwargs)`. Internally uses [`MessageIdRequest`](sinch/domains/conversation/models/v1/messages/internal/request/message_id_request.py). |
| `sinch.domains.conversation.models.message.responses.GetConversationMessageResponse` | [`ConversationMessageResponse`](sinch/domains/conversation/models/v1/messages/response/types/__init__.py) (Union of app/contact message response types) |
| `sinch.domains.conversation.models.message.requests.DeleteConversationMessageRequest` | `delete(message_id, messages_source=None, **kwargs)`. Internally uses [`MessageIdRequest`](sinch/domains/conversation/models/v1/messages/internal/request/message_id_request.py). |
| `sinch.domains.conversation.models.message.responses.DeleteConversationMessageResponse` | `None` (method returns `None`) |
| `sinch.domains.conversation.models.message.requests.ListConversationMessagesRequest` | `list()` with individual parameters: `conversation_id`, `contact_id`, `app_id`, `page_size`, `page_token`, `view`, `messages_source`, `only_recipient_originated` (signature aligned with V1 where available) |
| `sinch.domains.conversation.models.message.responses.ListConversationMessagesResponse` | Response type for `list()` (messages list, next_page_token) |

#### Replacement APIs

The Conversation domain API access remains `sinch_client.conversation`; message operations are under `sinch_client.conversation.messages`. Recipient is specified with exactly one of `contact_id` or `recipient_identities` (list of `{channel, identity}`).

##### Messages API

| Old method | New method in `conversation.messages` |
|------------|----------------------------------------|
| `send()` with `SendConversationMessageRequest` | Use convenience methods: `send_text_message()`, `send_card_message()`, `send_carousel_message()`, `send_choice_message()`, `send_contact_info_message()`, `send_list_message()`, `send_location_message()`, `send_media_message()`, `send_template_message()`<br>Or `send()` with `app_id`, `message` (dict or `SendMessageRequestBodyDict`), and either `contact_id` or `recipient_identities` |
| `get()` with `GetConversationMessageRequest` | `get()` with `message_id: str` parameter |
| `delete()` with `DeleteConversationMessageRequest` | `delete()` with `message_id: str` parameter |
| `list()` with `ListConversationMessagesRequest` | In Progress |
| — |  **New in V2:** `update()` with `message_id`, `metadata`, and optional `messages_source`|

##### Replacement APIs / attributes

| Old | New |
|-----|-----|
| `sinch_client.conversation.webhook` (REST: create, list, get, update, delete webhooks; models under `sinch.domains.conversation.models.webhook`, e.g. `CreateConversationWebhookRequest`, `SinchListWebhooksResponse`) | **Not available in V2.** The Conversation client only exposes `messages` and `sinch_events`; More features are planned for future releases. To validate and parse inbound Sinch Events payloads, use `sinch_client.conversation.sinch_events(callback_secret)`—see **Sinch Events** below. |

#### Sinch Events (Event Destinations payload models and package path)

| Old | New |
|-----|-----|
| — _(N/A)_ | `sinch.domains.conversation.models.v1.sinch_events` (package path for inbound payload models) |
| — | [`ConversationSinchEvent`](sinch/domains/conversation/sinch_events/v1/conversation_sinch_event.py) (handler: signature validation and `parse_event`) |
| — | `ConversationSinchEventPayload`, `ConversationSinchEventBase`, and concrete event types (e.g. `MessageInboundEvent`, `MessageDeliveryReceiptEvent`, `MessageSubmitEvent`) |

To obtain a Conversation Sinch Events handler: `sinch_client.conversation.sinch_events(callback_secret)` returns a [`ConversationSinchEvent`](sinch/domains/conversation/sinch_events/v1/conversation_sinch_event.py) instance; `handler.parse_event(request_body)` returns a `ConversationSinchEventPayload`.

```python
# New
handler = sinch_client.conversation.sinch_events("your_callback_secret")
event = handler.parse_event(request_body)
```

#### Request and response fields: callback URL → event destination target

| | Old | New |
|---|-----|-----|
| **Messages (`send`)** | `sinch.domains.conversation.models.message.requests.SendConversationMessageRequest` field `callback_url` | [`SendMessageRequest`](sinch/domains/conversation/models/v1/messages/internal/request/send_message_request.py) field `event_destination_target` |
| **Messages (methods)** | `ConversationMessage.send(..., callback_url=...)` | `sinch_client.conversation.messages.send()`, `send_text_message()`, and other `send_*_message()` methods with `event_destination_target=...` |
| **Send event** | `sinch.domains.conversation.models.event.requests.SendConversationEventRequest` field `callback_url` | `event_destination_target` on the V2 send-event request model when that API is exposed |

The Conversation HTTP API still expects the JSON field **`callback_url`**. In V2, use the Python parameter / model field `event_destination_target`; it is serialized as `callback_url` on the wire (same pattern as other domains, e.g. SMS).

<br>

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

<br>

### [`Numbers` (Virtual Numbers)](https://github.com/sinch/sinch-sdk-python/tree/main/sinch/domains/numbers)

##### Replacement APIs / attributes

| Old | New |
|-----|-----|
| `sinch_client.numbers.callbacks` (attribute) | `sinch_client.numbers.event_destinations` (attribute) |
| `numbers.callbacks.get_configuration()` (method) | `numbers.event_destinations.get()` (method) |
| `numbers.callbacks.update_configuration(hmac_secret)` (method) | `numbers.event_destinations.update(hmac_secret=hmac_secret)` (method) |

##### Replacement models

| Old class | New class |
|-----------|-----------|
| `UpdateNumbersCallbackConfigurationRequest` | `UpdateEventDestinationRequest` |
| `GetNumbersCallbackConfigurationResponse` | `EventDestinationResponse` |
| `UpdateNumbersCallbackConfigurationResponse` | `EventDestinationResponse` |

**Example:**

```python
# Old
config = sinch_client.numbers.callbacks.get_configuration()
sinch_client.numbers.callbacks.update_configuration("your_hmac_secret")

# New
config = sinch_client.numbers.event_destinations.get()
sinch_client.numbers.event_destinations.update(hmac_secret="your_hmac_secret")
```

##### Available and Active: method locations

| Old method | New method |
|------------|------------|
| `numbers.available.rent_any(...)`, `numbers.available.activate(...)`, `numbers.available.check_availability(...)`, `numbers.available.list(...)` | `numbers.rent_any(...)`, `numbers.rent(...)`, `numbers.check_availability(...)`, `numbers.search_for_available_numbers(...)` |
| `numbers.active.list(...)`, `numbers.active.get(...)`, `numbers.active.update(...)`, `numbers.active.release(...)` | `numbers.list(...)`, `numbers.get(...)`, `numbers.update(...)`, `numbers.release(...)` |

#### Sinch Events (Event Destinations payload models and package path)

| Old | New |
|-----|-----|
| — _(N/A)_ | `sinch.domains.numbers.sinch_events` (package path) |
| — | `NumberSinchEvent` (class, payload model) |

To obtain a Numbers Sinch Events handler: `sinch_client.numbers.sinch_events(callback_secret)` returns a `SinchEvents` instance; `handler.parse_event(request_body)` returns a `NumberSinchEvent`.


```python
# New
from sinch.domains.numbers.sinch_events.v1.events import NumberSinchEvent
handler = sinch_client.numbers.sinch_events("your_callback_secret")
event = handler.parse_event(request_body)  # event is a NumberSinchEvent
```

#### Request and response fields: callback URL → event destination target

| | Old | New |
|---|-----|-----|
| **Methods that accept the parameter** | Only `numbers.available.rent_any(..., callback_url=...)` | `numbers.rent(...)`, `numbers.rent_any(...)`, and `numbers.update(...)` accept `event_destination_target` |
| **Parameter name** | `callback_url` | `event_destination_target` |


##### Replacement request/response attributes

| Old | New |
|-----|-----|
| `RentAnyNumberRequest.callback_url` | `RentNumberRequest.event_destination_target`, `RentAnyNumberRequest.event_destination_target`, `UpdateNumberConfigurationRequest.event_destination_target` |
| `ActiveNumber` has no callback field | `ActiveNumber.event_destination_target` (response) |

**Example:**

```python
# Old
sinch_client.numbers.available.rent_any(
    region_code="US",
    type_="LOCAL",
    sms_configuration={...},
    voice_configuration={...},
    callback_url="https://example.com/events",
)

# New
sinch_client.numbers.rent_any(
    region_code="US",
    number_type="LOCAL",
    sms_configuration={...},
    voice_configuration={...},
    event_destination_target="https://example.com/events",
)
```
