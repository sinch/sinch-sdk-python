# Changelog

All notable changes to the **Sinch Python SDK** are documented in this file.

> **Tag legend**
> - `[feature]` — new capability
> - `[fix]` — bug fix
> - `[deprecation notice]` — will be removed in a future release
> - `[dependency]` — third-party library update
> - `[doc]` — documentation only
> - `[test]` — test coverage
> - `[refactor]` — internal restructuring
> - `[releasing]` — release infrastructure
> - `[design]` — API design change
> - `[tech]` — technical improvement

---

## v2.2.0 – unreleased

### SDK

- **[design]** Extra fields on request and response models now pass through unchanged by default (no camelCase/snake_case rewriting). A new `Configuration(legacy_extra_fields_normalization=True)` flag restores the previous auto-conversion behavior for callers who depend on it; the flag is transitional and will be removed in 3.0.

### Numbers

- **[refactor]** `voice_configuration`, `sms_configuration`, and `number_pattern` request fields are now typed Pydantic models instead of raw dicts with validators. Added `VoiceConfigurationCustom`/`ScheduledVoiceProvisioningCustom` response variants for unrecognized voice configuration types.

### Conversation

- **[feature]** Conversation Apps API: `create`, `get`, `list`, `update`, and `delete` operations, with full model, endpoints and unit/e2e test coverage.
- **[deprecation notice]** `ConversationProcessingMode` and `ConversationRetentionPolicyType` are deprecated; they are unused by the SDK and will be removed in 3.0.
- **[deprecation notice]** `ConversationMetadataReportView` is deprecated in favour of `ConversationMetadataReportViewType`; it will be removed in 3.0.
- **[deprecation notice]** `ConversationChannel` is deprecated in favour of `ConversationChannelType`; it will be removed in 3.0.

---

## v2.1.0 – 2026-06-30

### SDK

- **[feature]** OAuth token requests are now automatically retried (up to 3 times, with exponential backoff and jitter) when the authentication service is rate-limited (`HTTP 429`). 
- **[dependency]** Set up minimum version for `requests` to `>=2.0.0` to prevent pulling in versions with known vulnerabilities.
- **[fix]** Fixed a race condition in OAuth token creation and renewal under concurrent requests: `TokenManagerBase` now uses a lock with double-checked locking so the initial token is fetched exactly once, and a new `refresh_auth_token(used_token)` deduplicates concurrent renewals by only fetching when the stale token still matches the cached one.
- **[refactor]** `HTTPTransport` now prepares and authenticates requests in `request()`, so the new `send_request(request_data)` receives an already-prepared `HttpRequest` and acts as a pure I/O primitive, simplifying subclassing.
- **[deprecation notice]** `HTTPTransport.send(endpoint)` is deprecated in favour of `send_request(request_data)`; the legacy method still works for backward compatibility, but will be removed in 3.0.
- **[deprecation notice]** `TokenManagerBase.invalidate_expired_token()` and `handle_invalid_token()` (and the `TokenState.EXPIRED` value) are deprecated and will be removed in 3.0, as token renewal now goes through `refresh_auth_token()`.
- **[tech]** Removed unused GitHub environment secrets from CI workflow and simplified test fixtures to use hardcoded test values.
- **[refactor]** Consolidated the duplicated per-domain `BaseModelConfiguration` classes into three shared base classes in `sinch.core.models.internal` (`BaseConfigModel`, `SnakeCaseExtrasModel`, `CamelCaseDumpModel`).
- **[doc]** Improve README structure and content.


### SMS

- **[feature]** SMS Groups API: `create`, `list`, `get`, `update`, `replace`, `delete`, and `list_members` operations, with full model, endpoint, and unit test coverage (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#groups-api)).
- **[feature]** SMS Inbounds API: `get` and `list` operations, with full model, endpoint, and unit test coverage (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#inbounds-api)).
- **[design]** SMS Sinch Events inbound payload models unified with the Inbounds API: `MOTextSinchEvent`, `MOBinarySinchEvent`, `MOMediaSinchEvent`, `MediaBody`, and `MediaItem` removed from `sinch_events`; use `InboundMessage` (and its variants) from `sinch.domains.sms.models.v1.types` instead (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#sms-sinch-events)).


### Numbers

- **[feature]** `NumberSinchEvent` synchronized with the Numbers OAS spec: new `internal_failure_code` field, additional `status` values (`IN_REVIEW`, `BLOCKED`, `COMPLETED`, `REJECTED`, `EXPIRED`), a new `NUMBER_ORDER_PROCESSING` event type, and corrected event type `DEPROVISIONING_FROM_VOICE_PLATFORM` (previously `DEPROVISIONING_TO_VOICE_PLATFORM`).

---

## v2.0.1 – 2026-06-02

### SMS

- **[fix]** SMS paginator fix.

---

## v2.0.0 – 2026-03-31

### Breaking Changes

- see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#200)

### SDK

- **[design]** Requires explicit `sms_region` and `conversation_region` on `SinchClient` before using SMS and Conversation APIs (no silent US/EU defaults); runtime failure if unset.
- **[design]** The v1 asynchronous client and httpx-based async stack were removed; only synchronous `SinchClient` is supported.
- **[feature]** Automatic pagination via a shared `Paginator` pattern for paged list APIs.
- **[doc]** README and configuration tests clarify which credentials apply to each API.

### Conversation

- **[feature]** Messages API refresh: convenience send methods (`send_text_message()`, `send_card_message()`, `send_carousel_message()`, `send_choice_message()`, `send_contact_info_message()`, `send_list_message()`, `send_location_message()`, `send_media_message()`, `send_template_message()`), `list()` as a paginator, `update()`, `event_destination_target` (wires `callback_url`), and a `sinch_client.conversation.sinch_events(...)` helper for inbound event handling.
- **[feature]** Conversation Sinch Events (webhooks) support.
- **[design]** Conversation webhook REST client removed; handle inbound traffic via Sinch Events (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)).

### Numbers

- **[feature]** Flatter API (`rent`, `list`, `event_destinations`, and related entry points), `event_destination_target`, and a Numbers Sinch Events helper.
- **[feature]** Available Regions endpoint.
- **[feature]** Webhook helper validates the signing secret in `validate_signature_header()`.
- **[tech]** Numbers Events payloads are passed through without client-side pre-processing.

### Number Lookup

- **[feature]** Number Lookup v1 (lookup API, models, snippets, and E2E coverage).

### SMS

- **[design]** SMS client configuration and authentication paths refactored for project vs service-plan credentials, including delivery-report flows.
- **[feature]** SMS delivery reports models and pagination. `groups` and `inbounds` are planned for a future release (see migration guide).
- **[feature]** SMS Sinch Events (webhooks) support.
- **[doc]** SMS migration guide and Sinch events quickstart material.

### Verification

- **[design]** Verification V1 APIs are removed. V2 Verification support is planned in a future release (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)).

### Voice

- **[design]** Voice V1 APIs are removed. V2 Voice support is planned in a future release (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)).

### Others

- **[dependency]** Pydantic v2 (`pydantic = ">=2.0.0"`).
- **[releasing]** Ruff linter adoption and CI workflow updates.
- **[doc]** Snippets and Getting Started live under `examples/`.
- **[doc]** Docstring updates across Numbers, SMS, and Conversation.
- **[refactor]** Model, type, and class renames.
- **[tech]** Conversation, Numbers, and SMS models and endpoints resynchronized with OpenAPI specification.
- **[test]** E2E test infrastructure and refactoring; SMS batches test coverage.

---

## v1.1.4 – 2025-10-23

### SDK

- **[feature]** Python 3.13 and 3.14 support.
- **[releasing]** CI updates.

---

## v1.1.3 – 2025-09-11

### Voice

- **[fix]** DTMF conference fix.

---

## v1.1.2 – 2025-06-18

### Test

- **[test]** End-to-end tests disabled.
- **[test]** Tests and CI improvements.

### SDK

- **[fix]** Async authentication fixes.

### Chore

- **[doc]** README link updates.
- **[releasing]** CI and release-related updates.

---

## v1.1.1 – 2024-12-19

### SDK

- **[fix]** Remove aiohttp leftovers.

---

## v1.1.0 – 2024-12-19

### Chore

- **[releasing]** CI strategy updates.

### Verification

- **[feature]** Backwards-compatible Verification API update.

### SDK

- **[feature]** PyPI publishing and httpx/async HTTP stack.

### SMS

- **[feature]** SMS service plan API.

---

## v1.0.0 – 2024-05-20

### SDK

- **[feature]** Verification API.
- **[feature]** Voice API.

### Chore

- **[doc]** General availability README updates.
