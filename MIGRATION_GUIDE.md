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

##### Apps (create, get, list, update, delete)

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.app.requests.CreateConversationAppRequest` | `create()` with individual parameters: `channel_credentials`, `display_name` and optional `conversation_metadata_report_view`, `retention_policy`, `dispatch_retention_policy`, `processing_mode`, `smart_conversation`, `event_destination_settings`, `message_retry_settings`, `delivery_report_based_fallback`. Internally uses [`CreateAppRequest`](sinch/domains/conversation/models/v1/apps/request/create_app_request.py). |
| `sinch.domains.conversation.models.app.responses.CreateConversationAppResponse` | [`AppCustomResponse`](sinch/domains/conversation/models/v1/apps/response/app_custom_response.py) by default (`channel_credentials` keyed by channel). Pass `raw_response=True` to get [`AppResponse`](sinch/domains/conversation/models/v1/apps/response/app_response.py) (`channel_credentials` as the list returned by the API). |
| `sinch.domains.conversation.models.app.requests.GetConversationAppRequest` | `get(app_id, raw_response=False)` |
| `sinch.domains.conversation.models.app.responses.GetConversationAppResponse` | [`AppCustomResponse`](sinch/domains/conversation/models/v1/apps/response/app_custom_response.py) / [`AppResponse`](sinch/domains/conversation/models/v1/apps/response/app_response.py) (see `create()`) |
| `sinch.domains.conversation.models.app.responses.ListConversationAppsResponse` | `list(raw_response=False)` returns a `Paginator` of [`AppCustomResponse`](sinch/domains/conversation/models/v1/apps/response/app_custom_response.py) (or [`AppResponse`](sinch/domains/conversation/models/v1/apps/response/app_response.py) with `raw_response=True`) |
| `sinch.domains.conversation.models.app.requests.UpdateConversationAppRequest` | `update(app_id, ...)` with the same optional parameters as `create()`. `update_mask` is no longer a parameter: the SDK builds it from the fields you pass. Internally uses [`UpdateAppRequest`](sinch/domains/conversation/models/v1/apps/request/update_app_request.py). |
| `sinch.domains.conversation.models.app.responses.UpdateConversationAppResponse` | [`AppCustomResponse`](sinch/domains/conversation/models/v1/apps/response/app_custom_response.py) / [`AppResponse`](sinch/domains/conversation/models/v1/apps/response/app_response.py) (see `create()`) |
| `sinch.domains.conversation.models.app.requests.DeleteConversationAppRequest` | `delete(app_id)` |
| `sinch.domains.conversation.models.app.responses.DeleteConversationAppResponse` | `None` (method returns `None`) |

##### Contacts (create, get, list, update, delete, merge, channel profile)

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.contact.requests.CreateConversationContactRequest` | `create()` with individual parameters: `channel_identities`, `language` and optional `channel_priority`, `display_name`, `email`, `external_id`, `metadata` |
| `sinch.domains.conversation.models.contact.responses.CreateConversationContactResponse` | [`ContactResponse`](sinch/domains/conversation/models/v1/contacts/response/contact_response.py) |
| `sinch.domains.conversation.models.contact.requests.GetConversationContactRequest` | `get(contact_id)` |
| `sinch.domains.conversation.models.contact.responses.GetConversationContactResponse` | [`ContactResponse`](sinch/domains/conversation/models/v1/contacts/response/contact_response.py) |
| `sinch.domains.conversation.models.contact.requests.ListConversationContactRequest` | `list()` with the same fields as keyword arguments: `page_size`, `page_token`, `external_id`, `channel`, `identity` |
| `sinch.domains.conversation.models.contact.responses.ListConversationContactsResponse` | `Paginator` of [`ContactResponse`](sinch/domains/conversation/models/v1/contacts/response/contact_response.py) |
| `sinch.domains.conversation.models.contact.requests.UpdateConversationContactRequest` | `update(contact_id, ...)` with optional `channel_identities`, `channel_priority`, `display_name`, `email`, `external_id`, `language`, `metadata`. The SDK builds `update_mask` from the fields you pass. |
| `sinch.domains.conversation.models.contact.responses.UpdateConversationContactResponse` | [`ContactResponse`](sinch/domains/conversation/models/v1/contacts/response/contact_response.py) |
| `sinch.domains.conversation.models.contact.requests.DeleteConversationContactRequest` | `delete(contact_id)` |
| `sinch.domains.conversation.models.contact.responses.DeleteConversationContactResponse` | `None` (method returns `None`) |
| `sinch.domains.conversation.models.contact.requests.MergeConversationContactsRequest` | `merge_contact(destination_id, source_id, strategy=...)` |
| `sinch.domains.conversation.models.contact.responses.MergeConversationContactsResponse` | [`ContactResponse`](sinch/domains/conversation/models/v1/contacts/response/contact_response.py) (the preserved contact) |
| `sinch.domains.conversation.models.contact.requests.GetConversationChannelProfileRequest` | `get_channel_profile(app_id, channel, recipient)`, or the convenience methods `get_channel_profile_by_contact_id()` and `get_channel_profile_by_channel_identity()` |
| `sinch.domains.conversation.models.contact.responses.GetConversationChannelProfileResponse` | [`GetChannelProfileResponse`](sinch/domains/conversation/models/v1/contacts/response/get_channel_profile_response.py) |

##### Conversations (create, get, list, update, delete, stop, inject)

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.conversation.requests.CreateConversationRequest` | `create()` with individual parameters: `app_id`, `contact_id` and optional `active`, `active_channel`, `metadata_json`, `correlation_id`. V1 `conversation_metadata` is now `metadata_json`. V1 `id` and the deprecated `metadata` string are not accepted (the ID is generated by the API). |
| `sinch.domains.conversation.models.conversation.responses.SinchCreateConversationResponse` | [`ConversationResponse`](sinch/domains/conversation/models/v1/conversations/response/conversation_response.py) |
| `sinch.domains.conversation.models.conversation.requests.GetConversationRequest` | `get(conversation_id)` |
| `sinch.domains.conversation.models.conversation.responses.SinchGetConversationResponse` | [`ConversationResponse`](sinch/domains/conversation/models/v1/conversations/response/conversation_response.py) |
| `sinch.domains.conversation.models.conversation.requests.ListConversationsRequest` | `list()` with the same fields as keyword arguments: `app_id`, `contact_id`, `only_active`, `page_size`, `page_token`. V2 adds optional `active_channel`. |
| `sinch.domains.conversation.models.conversation.responses.SinchListConversationsResponse` | `Paginator` of [`ConversationResponse`](sinch/domains/conversation/models/v1/conversations/response/conversation_response.py) |
| `sinch.domains.conversation.models.conversation.requests.UpdateConversationRequest` | `update(conversation_id, ...)` with optional `active`, `active_channel`, `app_id`, `contact_id`, `metadata_json`, `correlation_id`, `metadata_update_strategy`. The SDK builds `update_mask` from the fields you pass. |
| `sinch.domains.conversation.models.conversation.responses.SinchUpdateConversationResponse` | [`ConversationResponse`](sinch/domains/conversation/models/v1/conversations/response/conversation_response.py) |
| `sinch.domains.conversation.models.conversation.requests.DeleteConversationRequest` | `delete(conversation_id)` |
| `sinch.domains.conversation.models.conversation.responses.SinchDeleteConversationResponse` | `None` (method returns `None`) |
| `sinch.domains.conversation.models.conversation.requests.StopConversationRequest` | `stop_active(conversation_id)` |
| `sinch.domains.conversation.models.conversation.responses.SinchStopConversationResponse` | `None` (method returns `None`) |
| `sinch.domains.conversation.models.conversation.requests.InjectMessageToConversationRequest` | `inject_message()` with individual parameters: `conversation_id`, `contact_id`, `channel_identity`, `direction`, `accept_time`, exactly one of `app_message` or `contact_message`, and optional `sender_id`, `processing_mode`, `metadata` |
| `sinch.domains.conversation.models.conversation.responses.SinchInjectMessageResponse` | `None` (method returns `None`) |

##### Events (send)

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.event.requests.SendConversationEventRequest` | `send()` with individual parameters: `app_id`, `event`, either `contact_id` or `recipient_identities`, and optional `event_destination_target`, `channel_priority_order`, `event_metadata`, `queue`. Internally uses [`SendEventRequest`](sinch/domains/conversation/models/v1/events/internal/send_event_request.py). |
| `sinch.domains.conversation.models.event.responses.SendConversationEventResponse` | [`SendEventResponse`](sinch/domains/conversation/models/v1/events/response/send_event_response.py) |

##### Webhooks → Event Destinations

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.webhook.requests.CreateConversationWebhookRequest` | `event_destinations.create()` with individual parameters: `app_id`, `target` and optional `client_credentials`, `secret`, `target_type`, `triggers` |
| `sinch.domains.conversation.models.webhook.responses.CreateWebhookResponse` | [`EventDestinationResponse`](sinch/domains/conversation/models/v1/event_destinations/response/event_destination_response.py) |
| `sinch.domains.conversation.models.webhook.requests.GetConversationWebhookRequest` | `event_destinations.get(event_destination_id)` |
| `sinch.domains.conversation.models.webhook.responses.GetWebhookResponse` | [`EventDestinationResponse`](sinch/domains/conversation/models/v1/event_destinations/response/event_destination_response.py) |
| `sinch.domains.conversation.models.webhook.requests.ListConversationWebhookRequest` | `event_destinations.list(app_id)` |
| `sinch.domains.conversation.models.webhook.responses.SinchListWebhooksResponse` | `Paginator` of [`EventDestinationResponse`](sinch/domains/conversation/models/v1/event_destinations/response/event_destination_response.py) |
| `sinch.domains.conversation.models.webhook.requests.UpdateConversationWebhookRequest` | `event_destinations.update(event_destination_id, ...)` with optional `app_id`, `target`, `client_credentials`, `secret`, `target_type`, `triggers`. The SDK builds `update_mask` from the fields you pass. |
| `sinch.domains.conversation.models.webhook.responses.UpdateWebhookResponse` | [`EventDestinationResponse`](sinch/domains/conversation/models/v1/event_destinations/response/event_destination_response.py) |
| `sinch.domains.conversation.models.webhook.requests.DeleteConversationWebhookRequest` | `event_destinations.delete(event_destination_id)` |
| `sinch.domains.conversation.models.webhook.responses.SinchDeleteWebhookResponse` | `None` (method returns `None`) |

##### Capability (lookup)

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.capability.requests.QueryConversationCapabilityRequest` | `lookup()` with individual parameters: `app_id`, either `contact_id` or `recipient_identities`, and optional `request_id` |
| `sinch.domains.conversation.models.capability.responses.QueryConversationCapabilityResponse` | [`LookupCapabilityResponse`](sinch/domains/conversation/models/v1/capability/response/lookup_capability_response.py) |

##### Transcoding

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.transcoding.requests.TranscodeConversationMessageRequest` | `transcode_message()` with the same fields as individual parameters: `app_id`, `app_message`, `channels` and optional `from_`, `to` |
| `sinch.domains.conversation.models.transcoding.responses.TranscodeConversationMessageResponse` | [`TranscodeMessageResponse`](sinch/domains/conversation/models/v1/transcoding/response/transcode_message_response.py) |

##### Templates

V1 targeted the Template Management API **v1** (`/v1/projects/{project_id}/templates`). V2 targets the Template Management API **v2** (`/v2/projects/{project_id}/templates`), whose model is different: translations are versioned and the V1 fields `channel`, `create_time` and `update_time` are no longer accepted on requests.

| Old class | New class |
|-----------|-----------|
| `sinch.domains.conversation.models.templates.requests.CreateConversationTemplateRequest` | `create()` with individual parameters: `default_translation`, `translations` and optional `id`, `description`, `version` |
| `sinch.domains.conversation.models.templates.responses.CreateConversationTemplateResponse` | [`TemplateResponse`](sinch/domains/conversation/templates/models/v2/response/template_response.py) |
| `sinch.domains.conversation.models.templates.requests.GetConversationTemplateRequest` | `get(template_id)` |
| `sinch.domains.conversation.models.templates.responses.GetConversationTemplateResponse` | [`TemplateResponse`](sinch/domains/conversation/templates/models/v2/response/template_response.py) |
| `sinch.domains.conversation.models.templates.responses.ListConversationTemplatesResponse` | `list()` returns a `Paginator` of [`TemplateResponse`](sinch/domains/conversation/templates/models/v2/response/template_response.py) |
| `sinch.domains.conversation.models.templates.requests.UpdateConversationTemplateRequest` | `update(template_id, version, ...)` with optional `default_translation`, `translations`, `description`. `version` (the current version of the template) is now required and `update_mask` is no longer a parameter. |
| `sinch.domains.conversation.models.templates.responses.UpdateConversationTemplateResponse` | [`TemplateResponse`](sinch/domains/conversation/templates/models/v2/response/template_response.py) |
| `sinch.domains.conversation.models.templates.requests.DeleteConversationTemplateRequest` | `delete(template_id)` |
| `sinch.domains.conversation.models.templates.responses.DeleteConversationTemplateResponse` | `None` (method returns `None`) |

#### Replacement APIs

The Conversation domain API access remains `sinch_client.conversation`. Its resources are exposed as `messages`, `apps`, `contacts`, `conversations`, `events`, `event_destinations`, `capability`, `transcoding`, `templates`, `consents` and `project_settings`, plus the `sinch_events()` handler factory. V1 singular attribute names (`message`, `app`, `contact`, `conversation`, `event`, `template`, `webhook`) are replaced by the plural names above. Wherever a recipient is required (`messages.send*()`, `events.send()`, `capability.lookup()`), it is specified with exactly one of `contact_id` or `recipient_identities` (list of `{channel, identity}`) instead of the V1 `recipient` dict.

All `list()` methods return a **`Paginator`**: use `.content()` for the items on the current page, `.next_page()` to load the next page, or `.iterator()` to walk every item across all pages.

##### Messages API

| Old method | New method in `conversation.messages` |
|------------|----------------------------------------|
| `send()` with `SendConversationMessageRequest` | Use convenience methods: `send_text_message()`, `send_card_message()`, `send_carousel_message()`, `send_choice_message()`, `send_contact_info_message()`, `send_list_message()`, `send_location_message()`, `send_media_message()`, `send_template_message()`<br>Or `send()` with `app_id`, `message` (dict or `SendMessageRequestBodyDict`), and either `contact_id` or `recipient_identities` |
| `get()` with `GetConversationMessageRequest` | `get()` with `message_id: str` parameter |
| `delete()` with `DeleteConversationMessageRequest` | `delete()` with `message_id: str` parameter |
| `list()` with `ListConversationMessagesRequest` | `list()` with the same fields as keyword arguments (see models table above). V2 adds optional `channel_identity`, `start_time`, `end_time`, `channel`, `direction`. Returns **`Paginator[ConversationMessageResponse]`**: use `.content()` for messages on the current page, `.next_page()` to load the next page, or `.iterator()` to walk every message across all pages. |
| — | **New in V2:** `update()` with `message_id`, `metadata`, and optional `messages_source` |

##### Apps API

| Old method in `conversation.app` | New method in `conversation.apps` |
|------------|----------------------------------------|
| `create()` with `CreateConversationAppRequest` fields | `create()` (see models table above). V2 adds optional `smart_conversation`, `event_destination_settings`, `message_retry_settings`, `delivery_report_based_fallback`. |
| `get(app_id)` | `get(app_id)` |
| `list()` | `list()`, returns a `Paginator` |
| `update()` with `UpdateConversationAppRequest` fields | `update()`, without `update_mask` |
| `delete(app_id)` | `delete(app_id)` |

##### Contacts API

| Old method in `conversation.contact` | New method in `conversation.contacts` |
|------------|----------------------------------------|
| `create()` | `create()` |
| `get(contact_id)` | `get(contact_id)` |
| `list()` | `list()`, returns a `Paginator` |
| `update()` | `update()` |
| `delete(contact_id)` | `delete(contact_id)` |
| `merge(source_id, destination_id, strategy)` | `merge_contact(destination_id, source_id, strategy=...)` |
| `get_channel_profile(app_id, recipient, channel)` | `get_channel_profile(app_id, channel, recipient)`, `get_channel_profile_by_contact_id(app_id, channel, contact_id)` or `get_channel_profile_by_channel_identity(app_id, channel, recipient_identities)` |
| — | **New in V2:** `list_identity_conflicts()`, returns a `Paginator` of [`ContactIdentityConflict`](sinch/domains/conversation/models/v1/contacts/response/contact_identity_conflict.py) |

##### Conversations API

| Old method in `conversation.conversation` | New method in `conversation.conversations` |
|------------|----------------------------------------|
| `create()` | `create()` (see models table above for the `metadata` / `conversation_metadata` changes) |
| `get(conversation_id)` | `get(conversation_id)` |
| `list()` | `list()`, returns a `Paginator` |
| `update()` | `update()`, without `update_mask` |
| `delete(conversation_id)` | `delete(conversation_id)` |
| `stop(conversation_id)` | `stop_active(conversation_id)` |
| `inject_message_to_conversation()` | `inject_message()` |
| — | **New in V2:** `list_recent(app_id, ...)`, returns a `Paginator` of [`RecentConversationResponse`](sinch/domains/conversation/models/v1/conversations/response/recent_conversation_response.py) |
| — | **New in V2:** `inject_event(conversation_id, app_event, accept_time, ...)`, returns [`InjectEventResponse`](sinch/domains/conversation/models/v1/conversations/response/inject_event_response.py) |

##### Events API

| Old method in `conversation.event` | New method in `conversation.events` |
|------------|----------------------------------------|
| `send(app_id, recipient, event, callback_url, ...)` | `send(app_id, event, contact_id=... or recipient_identities=..., event_destination_target=..., ...)` |
| — | **New in V2:** `get(event_id)`, returns [`ConversationEventResponse`](sinch/domains/conversation/models/v1/events/response/conversation_event_response.py) |
| — | **New in V2:** `list()` with `conversation_id`, `contact_id`, `page_size`, `page_token`, returns a `Paginator` of [`ConversationEventResponse`](sinch/domains/conversation/models/v1/events/response/conversation_event_response.py) |
| — | **New in V2:** `delete(event_id)` |

##### Event Destinations API

| Old method in `conversation.webhook` | New method in `conversation.event_destinations` |
|------------|----------------------------------------|
| `create()` | `create()` |
| `get(webhook_id)` | `get(event_destination_id)` |
| `list(app_id)` | `list(app_id)`, returns a `Paginator` |
| `update(webhook_id, ...)` | `update(event_destination_id, ...)`, without `update_mask` |
| `delete(webhook_id)` | `delete(event_destination_id)` |

##### Capability API

| Old method in `conversation.capability` | New method in `conversation.capability` |
|------------|----------------------------------------|
| `query(app_id, recipient, request_id)` | `lookup(app_id, contact_id=... or recipient_identities=..., request_id=...)` |

##### Transcoding API

| Old method in `conversation.transcoding` | New method in `conversation.transcoding` |
|------------|----------------------------------------|
| `transcode_message(app_id, app_message, channels, from_, to)` | `transcode_message(app_id, app_message, channels, from_, to)` (unchanged) |

##### Templates API

| Old method in `conversation.template` | New method in `conversation.templates` |
|------------|----------------------------------------|
| `create()` | `create()` (Template Management API v2, see models table above) |
| `get(template_id)` | `get(template_id)` |
| `list()` | `list()`, returns a `Paginator` |
| `update()` | `update(template_id, version, ...)` |
| `delete(template_id)` | `delete(template_id)` |
| — | **New in V2:** `list_translations(template_id, language_code=..., translation_version=...)`, returns a `Paginator` of [`TemplateTranslation`](sinch/domains/conversation/templates/models/v2/shared/template_translation.py) |

##### Consents API (new in V2)

| Old | New method in `conversation.consents` |
|-----|----------------------------------------|
| — | `list_identities(app_id, list_type, ...)`, returns a `Paginator` of [`ConsentIdentityResponse`](sinch/domains/conversation/models/v1/consents/response/consent_identity_response.py) |
| — | `list_audit_records(app_id, identity)`, returns [`AuditRecordsResponse`](sinch/domains/conversation/models/v1/consents/response/audit_records_response.py) |

##### Project Settings API (new in V2)

| Old | New method in `conversation.project_settings` |
|-----|----------------------------------------|
| — | `create(contact_settings)`, `get()`, `update(contact_settings)`, `delete()`. `create()`, `get()` and `update()` return [`ProjectSettingsResponse`](sinch/domains/conversation/models/v1/project_settings/response/project_settings_response.py). |

##### Replacement APIs / attributes

| Old | New |
|-----|-----|
| `sinch_client.conversation.webhook` | `sinch_client.conversation.event_destinations` (see **Event Destinations API** above). To validate and parse inbound Sinch Events payloads, use `sinch_client.conversation.sinch_events(callback_secret)`. See **Sinch Events** below. |
| `sinch_client.conversation.opt_in.register()` / `sinch_client.conversation.opt_out.register()` (models `RegisterConversationOptInRequest`, `RegisterConversationOptInResponse`, `RegisterConversationOptOutRequest`, `RegisterConversationOptOutResponse`) | **Not available in V2.** The opt-in/opt-out registration endpoints are no longer part of the Conversation API. To query consent lists use `sinch_client.conversation.consents`. `OPT_IN` / `OPT_OUT` notifications are still delivered to event destinations and parsed by `sinch_events()` as `OptInEvent` / `OptOutEvent`. |
| `sinch.domains.conversation.models.SinchConversationRecipient` (`recipient` dict) | `contact_id` or `recipient_identities` parameters |

#### Sinch Events (Event Destinations payload models and package path)

| Old | New |
|-----|-----|
| — _(N/A)_ | `sinch.domains.conversation.models.v1.sinch_events` (package path for inbound payload models) |
| — | [`ConversationSinchEvent`](sinch/domains/conversation/sinch_events/v1/conversation_sinch_event.py) (handler: signature validation and `parse_event`) |
| — | `ConversationSinchEventPayload`, `ConversationSinchEventBase`, and one concrete event type per trigger (see table below) |

`parse_event()` returns the concrete event type that matches the payload:

| Trigger | Event type |
|---------|------------|
| `MESSAGE_INBOUND` | `MessageInboundEvent` |
| `MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION` | `MessageInboundSmartConversationRedactionEvent` |
| `MESSAGE_SUBMIT` | `MessageSubmitEvent` |
| `MESSAGE_DELIVERY` | `MessageDeliveryReceiptEvent` |
| `EVENT_INBOUND` | `EventInboundEvent` |
| `EVENT_DELIVERY` | `EventDeliveryReceiptEvent` |
| `CONVERSATION_START` / `CONVERSATION_STOP` / `CONVERSATION_DELETE` | `ConversationStartEvent` / `ConversationStopEvent` / `ConversationDeleteEvent` |
| `CONTACT_CREATE` / `CONTACT_DELETE` / `CONTACT_UPDATE` / `CONTACT_MERGE` | `ContactCreateEvent` / `ContactDeleteEvent` / `ContactUpdateEvent` / `ContactMergeEvent` |
| `CONTACT_IDENTITIES_DUPLICATION` | `ContactIdentitiesDuplicationEvent` |
| `CAPABILITY` | `CapabilityEvent` |
| `OPT_IN` / `OPT_OUT` | `OptInEvent` / `OptOutEvent` |
| `CHANNEL_EVENT` | `ChannelEvent` |
| `RECORD_NOTIFICATION` | `RecordNotificationEvent` |
| `SMART_CONVERSATION` | `SmartConversationsEvent` |
| `UNSUPPORTED` | `UnsupportedSinchEvent` |

All of them can be imported from `sinch.domains.conversation.models.v1.sinch_events`.

> **Deprecation notice:** the modules under `sinch.domains.conversation.models.v1.sinch_events.events` (`conversation_sinch_event_base`, `conversation_sinch_event_payload`, `message_inbound_event`, `message_submit_event`, `message_submit_notification`, `inbound_message`, `message_delivery_receipt_event`, `message_delivery_report` and `delivery_status_type`) are kept as re-exports of their new locations and will be removed in 3.0. Import these classes from `sinch.domains.conversation.models.v1.sinch_events` instead.

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
| **Send event** | `sinch.domains.conversation.models.event.requests.SendConversationEventRequest` field `callback_url` | [`SendEventRequest`](sinch/domains/conversation/models/v1/events/internal/send_event_request.py) field `event_destination_target` |
| **Events (methods)** | `ConversationEvent.send(..., callback_url=...)` | `sinch_client.conversation.events.send(..., event_destination_target=...)` |
| **Apps** | — _(not exposed in V1)_ | `apps.create()` / `apps.update()` parameter `event_destination_settings` ([`EventDestinationSettings`](sinch/domains/conversation/models/v1/apps/shared/event_destination_settings.py), field `secret_for_overridden_target`) |

The Conversation HTTP API still expects the JSON fields **`callback_url`**, **`callback_settings`** and **`secret_for_overridden_callback_urls`**. In V2, use the Python parameters / model fields `event_destination_target`, `event_destination_settings` and `secret_for_overridden_target`; they are serialized with the original names on the wire (same pattern as other domains, e.g. SMS).

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
