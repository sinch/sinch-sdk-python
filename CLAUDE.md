# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the Sinch Python SDK, providing access to Sinch communication services (Numbers, SMS, Verification, Voice, and Conversation APIs). The SDK supports both synchronous and asynchronous operations with Python 3.9-3.12.

## Development Commands

### Setup
```bash
pip install -r requirements-dev.txt
```

### Testing
```bash
# Run all tests
pytest

# Run all tests with coverage
coverage run --source=. -m pytest

# View coverage report
python -m coverage report --skip-empty

# Run a single test file
pytest tests/unit/test_exceptions.py

# Run a specific test
pytest tests/unit/test_exceptions.py::test_sinch_validation_exception_not_from_remote_server

# Run tests in a specific domain
pytest tests/unit/domains/voice/
```

### Linting
```bash
# Lint the codebase (follows CI configuration)
flake8 sinch --count --max-complexity=10 --max-line-length=120 --statistics
```

### Environment Variables for Testing

Tests require Sinch credentials via environment variables:
- `KEY_ID`, `KEY_SECRET`, `PROJECT_ID` - OAuth/Basic auth
- `APPLICATION_KEY`, `APPLICATION_SECRET` - Signed auth
- `SERVICE_PLAN_ID`, `SMS_API_TOKEN` - SMS token auth
- Origin overrides: `NUMBERS_ORIGIN`, `SMS_ORIGIN`, `VERIFICATION_ORIGIN`, `VOICE_ORIGIN`, `CONVERSATION_ORIGIN`, `AUTH_ORIGIN`, `TEMPLATES_ORIGIN`
- `DISABLE_SSL` - For testing against local/dev environments
- `VOICE_CALL_ID` - For voice-specific tests

## Architecture

### Core Design Pattern

The SDK follows a **domain-driven, endpoint-based architecture** with clear separation between sync/async implementations:

1. **Client Layer** (`sinch/core/clients/`)
   - `SinchClient` (sync) uses `requests` library via `HTTPTransportRequests`
   - `SinchClientAsync` (async) uses `httpx` library via `HTTPXTransport`
   - Each client aggregates domain services (numbers, sms, verification, voice, conversation, authentication)
   - Custom HTTP transports can be injected by implementing `HTTPTransport` or `AsyncHTTPTransport` abstract base classes

2. **Domain Layer** (`sinch/domains/`)
   - Each domain (numbers, sms, verification, voice, conversation, authentication) has its own package
   - Domain classes provide high-level methods that instantiate endpoints and execute requests
   - Domains are instantiated with both sync and async variants (e.g., `Numbers` and `NumbersAsync`)

3. **Endpoint Layer** (`sinch/domains/*/endpoints/`)
   - Each API operation is a separate endpoint class inheriting from `HTTPEndpoint`
   - Endpoints define: `ENDPOINT_URL`, `HTTP_METHOD`, `HTTP_AUTHENTICATION`
   - Endpoints handle URL building, query params, request body serialization, and response deserialization
   - Authentication types: `BASIC`, `OAUTH`, `SIGNED` (HMAC), `SMS_TOKEN`

4. **Models Layer** (`sinch/domains/*/models/`)
   - Request models inherit from `SinchRequestBaseModel` (auto-excludes None values when serializing)
   - Response models inherit from `SinchBaseModel`
   - All models are dataclasses with `as_dict()` and `as_json()` helpers

5. **Transport Layer** (`sinch/core/ports/` and `sinch/core/adapters/`)
   - Abstract `HTTPTransport` and `AsyncHTTPTransport` define the contract
   - Concrete implementations: `HTTPTransportRequests` (sync) and `HTTPXTransport` (async)
   - Transport handles authentication, request preparation, and response handling
   - Token refresh for OAuth is handled automatically on 401 responses

### Authentication Flow

The SDK supports four authentication methods (see `sinch/core/enums.py`):
- **BASIC**: HTTP Basic Auth with `key_id:key_secret`
- **OAUTH**: Bearer token obtained via `TokenManager`/`TokenManagerAsync` from authentication endpoints
- **SIGNED**: HMAC signature using `application_key` and `application_secret` (see `sinch/core/signature.py`)
- **SMS_TOKEN**: Bearer token using `sms_api_token`

Token management (`sinch/core/token_manager.py`) caches access tokens and automatically refreshes on expiry.

### Pagination

Two pagination strategies in `sinch/core/pagination.py`:
- `IntBasedPaginator`/`AsyncIntBasedPaginator` - for page number based APIs
- `TokenBasedPaginator`/`AsyncTokenBasedPaginator` - for cursor/token based APIs (used by Numbers API)

Paginators are iterators that automatically fetch next pages until exhausted.

### Exception Hierarchy

- `SinchException` (base, in `sinch/core/exceptions.py`)
  - `ValidationException` - client-side validation failures
  - Domain-specific exceptions (e.g., `NumbersException`, `SMSException`) in `sinch/domains/*/exceptions.py`

All exceptions capture `is_from_server`, `message`, `http_response`, and `response_status_code`.

## Adding New Functionality

### Adding a New Endpoint

1. Create endpoint class in `sinch/domains/<domain>/endpoints/<subdomain>/<operation>.py`:
   ```python
   from sinch.core.endpoint import HTTPEndpoint
   from sinch.core.enums import HTTPAuthentication, HTTPMethods

   class MyNewEndpoint(HTTPEndpoint):
       ENDPOINT_URL = "{origin}/v1/projects/{project_id}/resource"
       HTTP_METHOD = HTTPMethods.POST.value
       HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

       def __init__(self, project_id: str, request_data: MyRequest):
           self.project_id = project_id
           self.request_data = request_data

       def build_url(self, sinch):
           return self.ENDPOINT_URL.format(
               origin=sinch.configuration.numbers_origin,
               project_id=self.project_id
           )

       def request_body(self):
           return self.request_data.as_json()

       def handle_response(self, response: HTTPResponse) -> MyResponse:
           # Deserialize response.body into MyResponse dataclass
           return MyResponse(**response.body)
   ```

2. Create request/response models in `sinch/domains/<domain>/models/<subdomain>/`

3. Add method to domain class in `sinch/domains/<domain>/__init__.py`:
   ```python
   def my_new_operation(self, param1: str) -> MyResponse:
       return self._sinch.configuration.transport.request(
           endpoint=MyNewEndpoint(
               project_id=self._sinch.configuration.project_id,
               request_data=MyRequest(param1=param1)
           )
       )
   ```

4. Implement async variant if adding to `NumbersAsync`, `SMSAsync`, etc.

### Adding a New Domain

1. Create package structure: `sinch/domains/<new_domain>/`
2. Add domain class with sync/async variants
3. Register domain in `SinchClient` and `SinchClientAsync` constructors
4. Create domain-specific exception in `exceptions.py`
5. Organize endpoints into logical subdirectories
6. Add configuration properties (e.g., origin URLs) to `sinch/core/clients/sinch_client_configuration.py`

## Testing Patterns

- Tests use `pytest` with `pytest-asyncio` for async test support
- Fixtures in `tests/conftest.py` provide shared test utilities
- Mock HTTP responses using dataclasses matching production models
- Test both sync and async variants where applicable
- Domain-specific tests in `tests/unit/domains/<domain>/`
- Core functionality tests in `tests/unit/`

## Package Management

Project uses Poetry for dependency management (`pyproject.toml`), but development uses pip with `requirements-dev.txt`.

## Logging

SDK uses Python's standard `logging` module with "Sinch" prefix. Configure via:
- Root logger (inherited by SDK)
- `logger_name` parameter (SDK uses specified logger)
- `logger` parameter (SDK uses provided logger instance)