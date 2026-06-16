# Sinch Python SDK

[![Python](https://img.shields.io/badge/python-blue.svg)](https://www.python.org/) [![Latest Release](https://img.shields.io/pypi/v/sinch?label=sinch&labelColor=FFC658)](https://pypi.org/project/sinch/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/sinch/sinch-sdk-python/blob/main/LICENSE)


Here you'll find documentation related to the Sinch Python SDK, including how to install it, initialize it, and start developing Python code using Sinch services.

To use Sinch services, you'll need a Sinch account and access keys. You can sign up for an account and create access keys at [dashboard.sinch.com](https://dashboard.sinch.com).

For more information on the SDK, refer to the dedicated [Python SDK documentation](https://developers.sinch.com/docs/sdks/python) section, and for the Sinch APIs on which this SDK is based, refer to the official [developer documentation portal](https://developers.sinch.com).


## Table of contents:

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Supported APIs](#supported-apis)
- [Getting started](#getting-started)
- [Logging](#logging)
- [Handling Exceptions](#handling-exceptions)
- [Custom HTTP client implementation](#custom-http-client-implementation)
- [Third-party dependencies](#third-party-dependencies)
- [Examples](#examples)
- [Changelog and Migration](#changelog--migration)
- [License](#license)
- [Contact](#contact)


## Prerequisites

- [Python](https://www.python.org/) in one of the supported versions - [3.9](https://www.python.org/downloads/release/python-390/), [3.10](https://www.python.org/downloads/release/python-3100/), [3.11](https://www.python.org/downloads/release/python-3110/), [3.12](https://www.python.org/downloads/release/python-3120/), [3.13](https://www.python.org/downloads/release/python-3130/), [3.14](https://www.python.org/downloads/release/python-3140/)
- [pip](https://pip.pypa.io/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)

> **Warning**:
> This SDK is intended for server-side (backend) use only. Do not use it in front-end or client-side applications (web, mobile, or desktop), regardless of language or framework. Doing so can expose your Sinch credentials to end-users.

## Installation

Run the following command to install the SDK:

```bash
pip install sinch
```


## Supported APIs


| API Category      | API Name                    |
|-------------------|-----------------------------|
| Messaging         | [Conversation API](#conversation-api) [[link]](https://developers.sinch.com/docs/conversation/)   |
| Messaging         | [SMS](#sms-api) [[link]](https://developers.sinch.com/docs/sms/)                                   |
| Numbers           | [Numbers API](#numbers-api) [[link]](https://developers.sinch.com/docs/numbers/)                   |
| Verification      | [Number Lookup API](#number-lookup-api) [[link]](https://developers.sinch.com/docs/number-lookup/) |


## Getting started


### Client initialization

To start using the SDK, initialize the main client class. This client gives you access to all the SDK services:

```python
import os
from sinch import SinchClient

# Warning: project authentication, check if the API used supports it or has additional parameters
sinch_client = SinchClient(
    project_id=os.environ["SINCH_PROJECT_ID"],
    key_id=os.environ["SINCH_KEY_ID"],
    key_secret=os.environ["SINCH_KEY_SECRET"],
)
```

Get `project_id`, `key_id` and `key_secret` from the [Access keys](https://dashboard.sinch.com/settings/access-keys) page in your Sinch dashboard (`key_secret` is shown only once, at creation time). It's highly recommended to not hardcode these credentials: load them from environment variables for local development, and from a secret manager in production.

This snippet is the common starting point for every API. Some APIs have a different initialization or need extra parameters (for example, a region), see the section for each API.

### Conversation API

The Conversation API is regionalized. To use this API, the `conversation_region` parameter is required:

```python
sinch_client = SinchClient(
    project_id=os.environ["SINCH_PROJECT_ID"],
    key_id=os.environ["SINCH_KEY_ID"],
    key_secret=os.environ["SINCH_KEY_SECRET"],
    conversation_region="eu",
)
```

#### Sinch Events

The Conversation API delivers asynchronous Sinch Events to the Event Destination URL you configure for your app in the [Conversation dashboard](https://dashboard.sinch.com/convapi/apps). `validate_authentication_header` confirms a request comes from Sinch and `parse_event` turns its payload into a typed event object; `headers` and `raw_body` are the incoming request's headers and raw body:

```python
sinch_events = sinch_client.conversation.sinch_events(SINCH_EVENT_SECRET)
is_valid = sinch_events.validate_authentication_header(headers=headers, json_payload=raw_body)
event = sinch_events.parse_event(raw_body, headers)
```

`SINCH_EVENT_SECRET` is optional and set per app in the [Conversation dashboard](https://dashboard.sinch.com/convapi/apps). `parse_event` works without validating the request, but then its origin can't be verified, so calling `validate_authentication_header` (which returns `True`/`False`) is recommended in production.

You can find a complete example in [examples/sinch_events/conversation_api](./examples/sinch_events/conversation_api).

### SMS API

> **Warning:** the SMS API is end-of-sale. For new integrations, prefer the [Conversation API](#conversation-api).

The SMS API is regionalized: set `sms_region` to the region where your SMS account is hosted. The accepted values are `us`, `eu`, `au`, `br` and `ca`, and the region also determines which credentials you can use:

- **Project access keys** — available only in the `us` and `eu` regions. Use the same `project_id`, `key_id` and `key_secret` as the common client, plus `sms_region`:

```python
sinch_client = SinchClient(
    project_id=os.environ["SINCH_PROJECT_ID"],
    key_id=os.environ["SINCH_KEY_ID"],
    key_secret=os.environ["SINCH_KEY_SECRET"],
    sms_region="us",
)
```

> **SMS authentication for new projects**
>
> Projects created after the SMS API end-of-sale (`15/04/26`) cannot use
> project access keys — the SMS API requests return `401 Unauthorized`.
>
> If you encounter this issue, consider the following options:
>
> 1. Use service plan credentials (`service_plan_id` + `sms_api_token`)
> 2. Use the Conversation API, which works with project access keys.
> 3. Contact your account manager


- **Service plan** — available in all regions (`us`, `eu`, `au`, `br`, `ca`). Use a `service_plan_id` and `sms_api_token`, both available on the [Service APIs dashboard](https://dashboard.sinch.com/sms/api/services):

```python
sinch_client = SinchClient(
    service_plan_id=os.environ["SINCH_SERVICE_PLAN_ID"],
    sms_api_token=os.environ["SINCH_SMS_API_TOKEN"],
    sms_region="us",
)
```

> **Note:** if you use both the SMS and the [Conversation API](#conversation-api)
> from the same client, set `sms_region` and `conversation_region` to the same
> region. Mismatched regions cause delivery failures.

#### Sinch Events

The SMS API delivers asynchronous Sinch Events to an Event Destination, whose URL is set per batch with the `event_destination_target` parameter on the send, update and replace operations (for example `sinch_client.sms.batches.send_sms`). `validate_authentication_header` confirms a request comes from Sinch and `parse_event` turns its payload into a typed event object; `headers` and `raw_body` are the incoming request's headers and raw body:

```python
sinch_events = sinch_client.sms.sinch_events(SINCH_EVENT_SECRET)
is_valid = sinch_events.validate_authentication_header(headers=headers, json_payload=raw_body)
event = sinch_events.parse_event(raw_body, headers)
```

Signature authentication for SMS events must be enabled for your account by your account manager; until then the signature headers are absent and `parse_event` can be used on its own. See the [SMS events documentation](https://developers.sinch.com/docs/sms/api-reference/sms/tag/Webhooks/#tag/Webhooks/section/Callbacks).

You can find a complete example in [examples/sinch_events/sms_api](./examples/sinch_events/sms_api).

### Numbers API

The Numbers API needs no extra parameters, use the [common client](#client-initialization) based in project authentication shown above.

#### Sinch Events

The Numbers API delivers asynchronous Sinch Events to the Event Destination you configure through `sinch_client.numbers.event_destinations`. `validate_authentication_header` confirms a request comes from Sinch and `parse_event` turns its payload into a typed event object; `headers` and `raw_body` are the incoming request's headers and raw body:

```python
sinch_events = sinch_client.numbers.sinch_events(SINCH_EVENT_SECRET)
is_valid = sinch_events.validate_authentication_header(headers=headers, json_payload=raw_body)
event = sinch_events.parse_event(raw_body, headers)
```

`SINCH_EVENT_SECRET` is the value configured on the Event Destination. `parse_event` works without validating the request, but then its origin can't be verified, so calling `validate_authentication_header` is recommended in production.

You can find a complete example in [examples/sinch_events/numbers_api](./examples/sinch_events/numbers_api).

### Number Lookup API

The Number Lookup API needs no extra parameters, use the [common client](#client-initialization) based in project authentication shown above.



### Your First Request

Once your client is configured, you can send your first message. The example below uses the Conversation API to send a simple text message over SMS. Replace CONVERSATION_APP_ID with your app ID and RECIPIENT_PHONE_NUMBER with the recipient's phone number:

```python
response = sinch_client.conversation.messages.send(
    app_id="CONVERSATION_APP_ID",
    message={
        "text_message": {
            "text": "[Python SDK: Conversation Message] Sample text message",
        },
    },
    recipient_identities=[
        {
            "channel": "SMS",
            "identity": "RECIPIENT_PHONE_NUMBER",
        }
    ],
)

print(f"Successfully sent message.\n{response}")
```

## Logging

Logging configuration for this SDK utilizes following hierarchy:
1. If no configuration was provided via `logger_name` or `logger` configurable, SDK will inherit configuration from the root logger with the `Sinch` prefix.
2. If `logger_name` configurable was provided, SDK will use logger related to that name. For example: `myapp.sinch` will inherit configuration from the `myapp` logger.
3. If `logger` (logger instance) configurable was provided, SDK will use that particular logger for all its logging operations.

If all logging returned by this SDK needs to be disabled, usage of `NullHandler` provided by the standard `logging` module is advised.

## Handling exceptions

Each API throws a custom, API related exception for an unsuccessful backed call.

Example for Numbers API:

```python
from sinch.domains.numbers.api.v1.exceptions import NumbersException

try:
    paginator = sinch_client.numbers.list(
        region_code="US",
        number_type="LOCAL",
    )
except NumbersException as err:
    pass
```

For handling all possible exceptions thrown by this SDK use `SinchException` (superclass of all Sinch exceptions) from `sinch.core.exceptions`.

## Custom HTTP client implementation

By default, the HTTP implementation uses the `requests` library.

To use a custom HTTP client, assign your transport to the client's configuration after initialization.

Custom transports must extend `HTTPTransport` and implement the `send` method. The base class provides `prepare_request` and `authenticate` helpers, and handles OAuth token refresh automatically.

The following example replaces the default `requests` backend with `httpx` and routes traffic through an authenticated proxy:

```python
import httpx
from sinch import SinchClient
from sinch.core.ports.http_transport import HTTPTransport
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse


class MyHTTPImplementation(HTTPTransport):
    def __init__(self, sinch, proxy_url, proxy_user, proxy_password):
        super().__init__(sinch)
        self.http_client = httpx.Client(
            proxy=f"http://{proxy_user}:{proxy_password}@{proxy_url}"
        )

    def send(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        request_data = self.prepare_request(endpoint)
        request_data = self.authenticate(endpoint, request_data)

        body = request_data.request_body
        response = self.http_client.request(
            method=request_data.http_method,
            url=request_data.url,
            json=body if isinstance(body, dict) else None,
            content=body if not isinstance(body, dict) else None,
            auth=request_data.auth,
            headers=request_data.headers,
            params=request_data.query_params,
            timeout=self.sinch.configuration.connection_timeout,
        )
        response_body = self.deserialize_json_response(response)

        return HTTPResponse(
            status_code=response.status_code,
            body=response_body,
            headers=dict(response.headers),
        )


sinch_client = SinchClient(
    key_id="key_id",
    key_secret="key_secret",
    project_id="some_project",
)
sinch_client.configuration.transport = MyHTTPImplementation(
    sinch_client,
    proxy_url="proxy.example.com:8080",
    proxy_user="proxy_user",
    proxy_password="proxy_password",
)
```

> **Note:** Asynchronous HTTP clients are not supported. The transport must be
> a synchronous implementation.


## Third-party dependencies
The SDK relies on the following third-party dependencies:
- [requests](https://requests.readthedocs.io/): HTTP client used as the default transport for all API calls.
- [pydantic](https://docs.pydantic.dev/): Data validation and serialization for request and response models.

## Examples

You can find:
 - a Python example of each request in the [examples/snippets](./examples/snippets) folder.
 - getting started guides for specific use cases in the [examples/getting-started](./examples/getting-started) folder.
 - server-side event handling examples in the [examples/sinch_events](./examples/sinch_events) folder.

## Changelog & Migration

For information about the latest changes in the SDK, please refer to the [CHANGELOG](CHANGELOG.md) file
and the [MIGRATION_GUIDE](MIGRATION_GUIDE.md) for instructions on how to update your code when upgrading to a new major version of the SDK.

## License

This project is licensed under the Apache License. 

See the [LICENSE](LICENSE) file for the license text.


## Contact

Developer Experience engineering team: [team-developer-experience@sinch.com](mailto:team-developer-experience@sinch.com)

