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

## v2.0.0 – 2026-03-31

### Major breaking changes with major release

- see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#200)

### SDK

- **[design]** Required explicit `sms_region` and `conversation_region` on `SinchClient` before using SMS and Conversation APIs (no silent US/EU defaults); runtime failure if unset (#49, #110).
- **[design]** The v1 asynchronous client and httpx-based async stack were removed; only synchronous `SinchClient` is supported (#55).
- **[feature]** Automatic pagination via a shared `Paginator` pattern for paged list APIs (#46, #54).
- **[doc]** README and configuration tests clarify which credentials apply to each API (#48).

### Conversation

- **[feature]** Messages API refresh: convenience send methods (`send_text_message()`, `send_card_message()`, `send_carousel_message()`, `send_choice_message()`, `send_contact_info_message()`, `send_list_message()`, `send_location_message()`, `send_media_message()`, `send_template_message()`), `list()` as a paginator, `update()`, `event_destination_target` (wires `callback_url`), and a `sinch_client.conversation.sinch_events(...)` helper for inbound event handling (#109–#120).
- **[feature]** Conversation Webhooks (#122), redesigned into Sinch Events (#131, #132, #133).
- **[deprecation notice]** Conversation webhook REST client surface removed; handle inbound traffic via Sinch Events (see migration guide) (#131, #132, #133).

### Numbers

- **[feature]** Flatter API (`rent`, `list`, `event_destinations`, and related entry points), `event_destination_target`, and a Numbers Sinch Events helper (#44, #53, #57, #58, #59, #62).
- **[feature]** Available Regions endpoint (#56).
- **[feature]** Webhook helper validates the signing secret in `validate_signature_header()` (#61).
- **[tech]** Numbers Events payloads are passed through without client-side pre-processing (#63).

### Number Lookup

- **[feature]** Number Lookup v1 (lookup API, models, snippets, and E2E coverage) (#99, #101, #104).

### SMS

- **[design]** SMS client configuration and authentication paths refactored for project vs service-plan credentials, including delivery-report flows (#90).
- **[feature]** SMS delivery reports models and pagination (#87). `groups` and `inbounds` are planned for a future release (see migration guide).
- **[feature]** SMS Sinch Events (webhooks) support (#103).
- **[doc]** SMS migration guide and Sinch events quickstart material (#107, #108).

### Verification

- **[design]** Verification V1 APIs are removed (#124). V2 Verification support is planned in a future release (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)).

### Voice

- **[design]** Voice V1 APIs are removed (#124). V2 Voice support is planned in a future release (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)).

### Others

- **[dependency]** Pydantic v2 (`pydantic = ">=2.0.0"`).
- **[releasing]** Ruff linter adoption (#84) and CI workflow updates (#121).
- **[doc]** Snippets and Getting Started live under `examples/` (#95, #98, #105, #106, #115, #118, #125, #127).
- **[doc]** Docstring updates across Numbers, SMS, and Conversation (#64, #65, #67, #96, #97).
- **[refactor]** Model, type, and class renames (#60, #70, #82).
- **[tech]** Conversation, Numbers, and SMS models and endpoints resynchronized with OpenAPI specification (#68, #75, #123, #128, #129, #134, #135).
- **[test]** E2E test infrastructure and refactoring (#45, #66, #102); SMS batches test coverage (#91, #93, #94).

---

## v1.1.4 – 2025-10-23

### SDK

- **[feature]** Python 3.13 and 3.14 support (#86, #89).
- **[releasing]** CI updates (#86, #89).

---

## v1.1.3 – 2025-09-11

### Voice

- **[fix]** DTMF conference fix (#79).

---

## v1.1.2 – 2025-06-18

### Test

- **[test]** End-to-end tests disabled.
- **[test]** Tests and CI improvements (#41, #42, #43, #74).

### SDK

- **[fix]** Async authentication fixes (#41, #42, #43, #74).

### Chore

- **[doc]** README link updates.
- **[releasing]** CI and release-related updates.

---

## v1.1.1 – 2024-12-19

### SDK

- **[fix]** Remove aiohttp leftovers (#40).

---

## v1.1.0 – 2024-12-19

### Chore

- **[releasing]** CI strategy updates (#34, #36, #29, #17).

### Verification

- **[feature]** Backwards-compatible Verification API update.

### SDK

- **[feature]** PyPI publishing and httpx/async HTTP stack.

### SMS

- **[feature]** SMS service plan API.

---

## v1.0.0 – 2024-05-20

### SDK

- **[feature]** Verification API (#26, #27, #28).
- **[feature]** Voice API (#26, #27, #28).

### Chore

- **[doc]** General availability README updates (#26, #27, #28).
