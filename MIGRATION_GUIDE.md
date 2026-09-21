# Sinch Python SDK Migration Guide

## 2.1.0

This release removes legacy SDK support.

This guide lists all removed classes and interfaces from V1 and how to migrate to their V2 equivalents.

> **Note:** Verification is not yet covered by the new V2 APIs. Support will be added in future releases.

---

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

---

### Voice Region

**In V1:**
```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="your-project-id",
    key_id="your-key-id",
    key_secret="your-key-secret",
)

sinch_client.configuration.voice_region = "use1"
```
- `voice_region` could only be set through the configuration object, as a plain string, after client initialization.

**In V2:**
- `voice_region` is exposed on `SinchClient` and on the configuration object, now using the `VoiceRegionEnum` enum instead of a plain string. It **defaults to `GLOBAL`**, so Voice V2 calls work out without setting it explicitly. Set it only if you need to pin calls to a specific region.

```python
from sinch import SinchClient
from sinch.core.enums import VoiceRegionEnum

sinch_client = SinchClient(
    project_id="your-project-id",
    key_id="your-key-id",
    key_secret="your-key-secret",
    voice_region=VoiceRegionEnum.EUROPE,
)

# Note: voice_region can also be set through the configuration object,
# but you must ensure this setting is done BEFORE any Voice API call:
sinch_client.configuration.voice_region = VoiceRegionEnum.EUROPE
```

---

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

---

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
| `list()` with `ListConversationMessagesRequest` | `list()` with the same fields as keyword arguments (see models table above). V2 adds optional `channel_identity`, `start_time`, `end_time`, `channel`, `direction`. Returns **`Paginator[ConversationMessageResponse]`**: use `.content()` for messages on the current page, `.next_page()` to load the next page, or `.iterator()` to walk every message across all pages. |
| — | **New in V2:** `update()` with `message_id`, `metadata`, and optional `messages_source` |

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

---

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

The SMS domain API access remains the same: `sinch.sms.batches`, `sinch.sms.delivery_reports`, `sinch.sms.inbounds` and `sinch.sms.groups`. However, the underlying models and method signatures have changed. See the sections below for the full list of changes: [Batches](#batches-api), [Delivery Reports](#delivery-reports-api), [Groups](#groups-api), [Inbounds](#inbounds-api).

##### Batches API

| Old method | New method in `sms.batches` |
|------------|----------------------------|
| `send()` with `SendBatchRequest` | Use convenience methods: `send_sms()`, `send_binary()`, `send_mms()`<br>Or `send()` with `SendSMSRequest` (Union of `TextRequest`, `BinaryRequest`, `MediaRequest`) |
| `list()` with `ListBatchesRequest` | `list()` with individual parameters: `page`, `page_size`, `start_date`, `end_date`, `from_`, `client_reference` |
| `get()` with `GetBatchRequest` | `get()` with `batch_id: str` parameter |
| `send_dry_run()` with `BatchDryRunRequest` | Use convenience methods: `dry_run_sms()`, `dry_run_binary()`, `dry_run_mms()`<br>Or `dry_run()` with `DryRunRequest` (Union of `DryRunTextRequest`, `DryRunBinaryRequest`, `DryRunMediaRequest`) |
| `update()` with `UpdateBatchRequest` | Use convenience methods: `update_sms()`, `update_binary()`, `update_mms()`<br>Or `update()` with `UpdateBatchMessageRequest` (Union of `UpdateTextRequestWithBatchId`, `UpdateBinaryRequestWithBatchId`, `UpdateMediaRequestWithBatchId`) |
| `replace()` with `ReplaceBatchRequest` | Use convenience methods: `replace_sms()`, `replace_binary()`, `replace_mms()`<br>Or `replace()` with `ReplaceBatchRequest` (Union of `ReplaceTextRequest`, `ReplaceBinaryRequest`, `ReplaceMediaRequest`) |

---

##### Delivery Reports API

| Old method | New method in `sms.delivery_reports` |
|------------|-------------------------------------|
| `list()` with `ListSMSDeliveryReportsRequest` | `list()` the parameters `start_date` and `end_date` now accepts both `str` and `datetime` |
| `get_for_batch()` with `GetSMSDeliveryReportForBatchRequest` | `get()` with `batch_id: str` and optional parameters: `report_type`, `status`, `code`, `client_reference` |
| `get_for_number()` with `GetSMSDeliveryReportForNumberRequest` | `get_for_number()` with `batch_id: str` and `recipient: str` parameters |

##### Groups API

###### Replacement models

| Old class | New class |
|-----------|-----------|
| `sinch.domains.sms.models.groups.requests.CreateSMSGroupRequest` | [`sinch.domains.sms.models.v1.internal.GroupRequest`](sinch/domains/sms/models/v1/internal/group_request.py) |
| `sinch.domains.sms.models.groups.requests.ListSMSGroupRequest` | [`sinch.domains.sms.models.v1.internal.ListGroupsRequest`](sinch/domains/sms/models/v1/internal/list_groups_request.py) |
| `sinch.domains.sms.models.groups.requests.GetSMSGroupRequest` | [`sinch.domains.sms.models.v1.internal.GroupIdRequest`](sinch/domains/sms/models/v1/internal/group_id_request.py) |
| `sinch.domains.sms.models.groups.requests.DeleteSMSGroupRequest` | [`sinch.domains.sms.models.v1.internal.GroupIdRequest`](sinch/domains/sms/models/v1/internal/group_id_request.py) |
| `sinch.domains.sms.models.groups.requests.GetSMSGroupPhoneNumbersRequest` | [`sinch.domains.sms.models.v1.internal.GroupIdRequest`](sinch/domains/sms/models/v1/internal/group_id_request.py) |
| `sinch.domains.sms.models.groups.requests.UpdateSMSGroupRequest` | [`sinch.domains.sms.models.v1.internal.UpdateGroupRequest`](sinch/domains/sms/models/v1/internal/update_group_request.py) |
| `sinch.domains.sms.models.groups.requests.ReplaceSMSGroupPhoneNumbersRequest` | [`sinch.domains.sms.models.v1.internal.ReplaceGroupRequest`](sinch/domains/sms/models/v1/internal/replace_group_request.py) |
| `sinch.domains.sms.models.groups.responses.CreateSMSGroupResponse` | [`sinch.domains.sms.models.v1.response.GroupResponse`](sinch/domains/sms/models/v1/response/group_response.py) |
| `sinch.domains.sms.models.groups.responses.GetSMSGroupResponse` | [`sinch.domains.sms.models.v1.response.GroupResponse`](sinch/domains/sms/models/v1/response/group_response.py) |
| `sinch.domains.sms.models.groups.responses.UpdateSMSGroupResponse` | [`sinch.domains.sms.models.v1.response.GroupResponse`](sinch/domains/sms/models/v1/response/group_response.py) |
| `sinch.domains.sms.models.groups.responses.ReplaceSMSGroupResponse` | [`sinch.domains.sms.models.v1.response.GroupResponse`](sinch/domains/sms/models/v1/response/group_response.py) |
| `sinch.domains.sms.models.groups.responses.SinchListSMSGroupResponse` | [`sinch.domains.sms.models.v1.response.ListGroupsResponse`](sinch/domains/sms/models/v1/response/list_groups_response.py) |
| `sinch.domains.sms.models.groups.responses.SinchGetSMSGroupPhoneNumbersResponse` | [`sinch.domains.sms.models.v1.response.ListGroupMembersResponse`](sinch/domains/sms/models/v1/response/list_group_members_response.py) |
| `sinch.domains.sms.models.groups.responses.SinchDeleteSMSGroupResponse` | `None` (method returns `None`) |

###### Replacement APIs

| Old method | New method in `sms.groups` |
|------------|---------------------------|
| `create()` with `CreateSMSGroupRequest` | `create()` with individual parameters: `name`, `members`, `child_groups`, `auto_update` |
| `list()` with `ListSMSGroupRequest` | `list()` with individual parameters: `page`, `page_size`. Returns **`Paginator[GroupResponse]`** |
| `get()` with `GetSMSGroupRequest` | `get()` with `group_id: str` parameter |
| `update()` with `UpdateSMSGroupRequest` | `update()` with `group_id: str` and optional parameters: `add`, `remove`, `name`, `add_from_group`, `remove_from_group`, `auto_update` |
| `replace()` with `ReplaceSMSGroupPhoneNumbersRequest` | `replace()` with `group_id: str` and optional parameters: `name`, `members`, `child_groups`, `auto_update` |
| `delete()` with `DeleteSMSGroupRequest` | `delete()` with `group_id: str` parameter |
| `get_phone_numbers()` / phone number listing | `list_members()` with `group_id: str`. Returns **`Paginator[str]`** |

##### Inbounds API

###### Replacement models

| Old class | New class |
|-----------|-----------|
| `sinch.domains.sms.models.inbounds.requests.ListSMSInboundMessageRequest` | [`sinch.domains.sms.models.v1.internal.ListInboundsRequest`](sinch/domains/sms/models/v1/internal/list_inbounds_request.py) |
| `sinch.domains.sms.models.inbounds.requests.GetSMSInboundMessageRequest` | [`sinch.domains.sms.models.v1.internal.InboundIdRequest`](sinch/domains/sms/models/v1/internal/inbound_id_request.py) |
| `sinch.domains.sms.models.inbounds.responses.SinchListInboundMessagesResponse` | [`sinch.domains.sms.models.v1.internal.ListInboundsResponse`](sinch/domains/sms/models/v1/internal/list_inbounds_response.py) |
| `sinch.domains.sms.models.inbounds.responses.GetInboundMessagesResponse` | [`sinch.domains.sms.models.v1.types.InboundMessage`](sinch/domains/sms/models/v1/types/inbound_message.py) (Union of `MOTextMessage`, `MOBinaryMessage`, `MOMediaMessage`) |

###### Replacement APIs

| Old method | New method in `sms.inbounds` |
|------------|------------------------------|
| `list()` with `ListSMSInboundMessageRequest` | `list()` with individual parameters: `page`, `page_size`, `to`, `start_date`, `end_date`, `client_reference`. Returns **`Paginator[InboundMessage]`** |
| `get()` with `GetSMSInboundMessageRequest` | `get()` with `inbound_id: str` parameter |

##### SMS Sinch Events

The inbound payload models in `sinch_events` have been unified with the Inbounds API models. The following classes have been removed:

| Removed class | Replacement |
|---------------|-------------|
| `sinch.domains.sms.sinch_events.v1.events.MOTextSinchEvent` | [`sinch.domains.sms.models.v1.shared.MOTextMessage`](sinch/domains/sms/models/v1/shared/mo_text_message.py) |
| `sinch.domains.sms.sinch_events.v1.events.MOBinarySinchEvent` | [`sinch.domains.sms.models.v1.shared.MOBinaryMessage`](sinch/domains/sms/models/v1/shared/mo_binary_message.py) |
| `sinch.domains.sms.sinch_events.v1.events.MOMediaSinchEvent` | [`sinch.domains.sms.models.v1.shared.MOMediaMessage`](sinch/domains/sms/models/v1/shared/mo_media_message.py) |
| `sinch.domains.sms.sinch_events.v1.events.MediaBody` | Embedded in `MOMediaMessage` |
| `sinch.domains.sms.sinch_events.v1.events.MediaItem` | Embedded in `MOMediaMessage` |

`IncomingSMSSinchEvent` is now a type alias for [`InboundMessage`](sinch/domains/sms/models/v1/types/inbound_message.py) (discriminated union of `MOTextMessage`, `MOBinaryMessage`, `MOMediaMessage`). Code that previously type-checked against `MOTextSinchEvent` and siblings should switch to their `MO*Message` equivalents.

---

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

---

### [`Voice`](https://github.com/sinch/sinch-sdk-python/tree/main/sinch/domains/voice)

#### Overview

Voice V1 has been fully removed. Voice V2 is a different call model built around SVAML commands (`answer`, `dial`, `bridge`, `hangup`, `menu`, `say`, etc.) instead of dedicated callout/conference objects. All V2 access goes through a new `.v2` segment: **`sinch_client.voice.v2.*`**. See [Voice Region](#voice-region) above for the `voice_region` parameter.

`sinch_client.voice.v2` exposes sub-APIs — `calls`, `batches`, `services`, `sessions`, `svaml` and  `sinch_events` for inbound webhook handling.

#### Replacement APIs / attributes

| Old | New |
|-----|-----|
| `sinch_client.voice.callouts` (`text_to_speech()`, `conference()`, `custom()`) | `sinch_client.voice.v2.calls.start(commands=[...])` — the call's behavior (PSTN callout, TTS, conference bridge, custom) is expressed via SVAML `commands`, not via separate methods |
| `sinch_client.voice.calls` (`get()`, `update()`, `manage_with_call_leg()`) | `sinch_client.voice.v2.calls` (`get()`, `list()`, `interact_by_call_id()`, `interact_by_call_name()`) |
| `sinch_client.voice.conferences` (`call()`, `get()`, `kick_all()`, `kick_participant()`, `manage_participant()`) | No dedicated conference object. Bridge/dial multiple legs together using SVAML `dial`/`bridge` commands passed to `calls.start()` / `calls.interact_by_call_id()` |
| `sinch_client.voice.applications` (number assignment: `get_numbers()`, `assign_numbers()`, `unassign_number()`, `query_number()`) | Not supported for Voice V2. Number assignment must be managed from the [Sinch Dashboard](https://dashboard.sinch.com/) instead |
| `sinch_client.voice.applications` (`get_callback_urls()`, `update_callback_urls()`) | Callback/webhook configuration is now managed at the **service** level via `sinch_client.voice.v2.services` — set `call_behavior` (type `EVENT_DESTINATION`) with an `event_destination`/`webhook` config when creating or updating a service, instead of per-number callback URLs |
| — | **New in V2:** `sinch_client.voice.v2.batches` (bulk/templated calling) and `sinch_client.voice.v2.services` (project-level call behavior and event destination configuration) |

##### Calls API

| Old method | New method in `voice.v2.calls` |
|------------|--------------------------------|
| `callouts.text_to_speech()`, `callouts.conference()`, `callouts.custom()` | `start(commands: List[SvamlCommandDict], service_id=None, idempotency_key=UNSET)` — outbound call creation, behavior defined by SVAML commands |
| `calls.get(call_id)` | `get(call_id: str) -> Call` |
| — | **New:** `list(service_id=None, from_=None, to=None, call_type=None, start_time=None, end_time=None, call_result=None, call_reason=None, page_size=None, page=None)`. Returns **`Paginator[Call]`** |
| `calls.update(call_id, instructions, action)` | `interact_by_call_id(call_id: str, commands: List[SvamlCommandDict], idempotency_key=UNSET) -> None` |
| `calls.manage_with_call_leg(call_id, call_leg, instructions, action)` | `interact_by_call_name(session_id: str, call_name: str, commands: List[SvamlCommandDict], idempotency_key=UNSET) -> None` |

##### Batches API (new in V2)

Batches queue many calls at once from a single set of SVAML `commands`, with per-call `parameters` interpolated into the commands via `@param_name` placeholders (e.g. `"phone": {"number": "@to_number"}`).

| Method in `voice.v2.batches` | Description |
|-------------------------------|--------------|
| `start(commands: List[SvamlCommandDict], parameters: List[Dict[str, str]], service_id=None, batch_options=UNSET, idempotency_key=UNSET) -> StartBatchResponse` | Start a batch of calls |
| `get(batch_id: str) -> BatchSummaryResponse` | Get batch summary |
| `get_details(batch_id: str) -> BatchDetailsResponse` | Get per-call batch details |
| `stop(batch_id: str) -> BatchStopResponse` | Stop a running batch |

##### Services API (new in V2)

A "service" configures how calls are handled for a project (default webhooks, event destinations, call behavior). There is no V1 equivalent.

| Method in `voice.v2.services` | Description |
|-------------------------------|--------------|
| `create(name: str, description=UNSET, is_default=UNSET, call_behavior=UNSET, idempotency_key=UNSET) -> ServiceResponse` | Create a service |
| `list(filter=None, is_default=None, page_size=None, page=None)` | Returns **`Paginator[ServiceShortResponse]`** |
| `get(service_id: str) -> ServiceResponse` | Get a service |
| `update(service_id: str, name=UNSET, description=UNSET, is_default=UNSET, call_behavior=UNSET, idempotency_key=UNSET) -> ServiceResponse` | Update a service |
| `delete(service_id: str) -> None` | Delete a service |

##### Sessions API (new in V2)

A session groups related call legs (e.g. all legs of a bridged call) and their states.

| Method in `voice.v2.sessions` | Description |
|--------------------------------|--------------|
| `get(session_id: str) -> SessionResponse` | Get a session |

##### Svaml API (new in V2)

Validate and describe a SVAML payload without creating a call — useful for checking the structure/flow of `commands` ahead of time.

| Method in `voice.v2.svaml` | Description |
|------------------------------|--------------|
| `validate(commands: List[SvamlCommandDict], call_name=UNSET, on_hangup=UNSET, validation_type=UNSET) -> ValidateSvamlResponse` | Validate a SVAML payload's structure/content, optionally in `strict`/`normal` mode via `validation_type` |
| `describe(commands: List[SvamlCommandDict], call_name=UNSET, on_hangup=UNSET) -> DescribeSvamlResponse` | Get a human-readable description of the commands, events, and messages defined in a SVAML payload |

#### Sinch Events (inbound webhook handling)

Access is via **`sinch_client.voice.v2.sinch_events`**.

| Method | Description |
|--------|--------------|
| `validate_authentication_header(method, path, headers, body, service_id, service_secret) -> bool` | Validates the inbound request's Authorization header |
| `parse_event(event_body, headers=None) -> VoiceSinchEventRequest` | Parses the inbound JSON/bytes/dict payload |
| `build_response(commands: List[SvamlCommandDict]) -> VoiceSinchEventResponse` | Builds a SVAML response to return to Sinch |
| `build_incoming_call_response(commands, call_name=UNSET, on_hangup=UNSET) -> VoiceSinchEventResponse` | Specialized builder for `call.incoming` events |
| `serialize_response(response: VoiceSinchEventResponse) -> Dict[str, Any]` | Serializes the response for the HTTP reply |

```python
# New
sinch_events_service = sinch_client.voice.v2.sinch_events

is_valid_request = sinch_events_service.validate_authentication_header(
    method=method, path=path, headers=headers, body=raw_body,
    service_id=service_id, service_secret=service_secret,
)
if not is_valid_request:
    return Response(status=401)

voice_event_request = sinch_events_service.parse_event(raw_body, headers)

voice_event_response = sinch_events_service.build_response(
    commands=[
        {
            "command": "messages",
            "messages": [
                {
                    "type": "SAY",
                    "say": {
                        "text": "Hello from Sinch!",
                        "voice_name": "Emma",
                    },
                },
            ],
        },
    ],
)
return jsonify(sinch_events_service.serialize_response(voice_event_response)), 200
```
