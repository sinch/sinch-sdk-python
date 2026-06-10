# Sinch Python SDK

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-3140/)

[![Latest Release](https://img.shields.io/pypi/v/sinch?label=sinch&labelColor=FFC658)](https://pypi.org/project/sinch/)


[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/sinch/sinch-sdk-python/blob/main/LICENSE)


Here you'll find documentation related to the Sinch Python SDK, including how to install it, initialize it, and start developing Python code using Sinch services.

To use Sinch services, you'll need a Sinch account and access keys. You can sign up for an account and create access keys at [dashboard.sinch.com](https://dashboard.sinch.com).

For more information on the SDK, refer to the dedicated [Python SDK documentation](https://developers.sinch.com/docs/sdks/python) section and for the Sinch APIs on which this SDK is based,official [developer documentation portal](https://developers.sinch.com).

## Table of contents:

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Getting started](#getting-started)
- [Supported APIs](#supported-apis)
- [Logging](#logging)
- [Handling Exceptions](#handling-exceptions)
- [Custom HTTP client implementation](#custom-http-client-implementation)
- [Third-party dependencies](#third-party-dependencies)
- [Examples](#examples)
- [Changelog and Migration](#changelog--migration)
- [License](#license)
- [Contact](#contact)


## Prerequisites

- [Python](https://www.python.org/) in one of the supported versions - 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
- [pip](https://pip.pypa.io/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)

## Installation

Run the following command to install the SDK:

```bash
pip install sinch
```


## Getting started


### Client initialization

To start using the SDK, you need to initialize the main client class with your credentials from your Sinch dashboard.
It's highly recommended to not hardcode these credentials and to load them from environment variables instead.

From this client, you have access to all the SDK services:

```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="project_id",
    key_id="key_id",
    key_secret="key_secret",
)
```

### Authentication


#### Project-level Authentication
This is the recommended, default method and the one most Sinch APIs rely on. It uses your project-level [access key](https://dashboard.sinch.com/settings/access-keys). The SDK exchanges them for a short-lived OAuth2 access token and refreshes it automatically.


```python
import os
from sinch import SinchClient

sinch_client = SinchClient(
    project_id=os.environ["SINCH_PROJECT_ID"],
    key_id=os.environ["SINCH_KEY_ID"],
    key_secret=os.environ["SINCH_KEY_SECRET"],
    # Set the region for the regionalized API(s)
    conversation_region="eu",
    sms_region="eu",
)
```

**Region parameters**

Some APIs are regionalized and require you to set their region explicitly. Since
v2.0.0 these parameters have no default, and the SDK raises a runtime error if
you call the API without setting them first (see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
for the upgrade details):

- `conversation_region` — required for the Conversation API.
- `sms_region` — required for the SMS API (detailed under [SMS Authentication](#sms-authentication)).

Pass them when you initialize `SinchClient` (as above). They can also be set
afterwards on the `configuration` object, but this must be done before the
first call to that API:

> **Note:** if you use both the SMS and Conversation APIs, `sms_region` and
> `conversation_region` must point to the same region. Mismatched regions
> cause delivery failures.


#### SMS authentication

The SMS API supports two authentication schemes depending on your region:

- **OAuth2 (US and EU)** — Uses the same project-level [access keys](https://dashboard.sinch.com/settings/access-keys) as above (`projectId`, `keyId`, `keySecret`).

```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="project_id",
    key_id="key_id",
    key_secret="key_secret",
    sms_region="us"
)
```

- **Service plan (AU, BR, CA, US and EU)** — Uses a `servicePlanId` and `apiToken` from the [Service APIs dashboard](https://dashboard.sinch.com/sms/api/services).


```python
from sinch import SinchClient

sinch_client = SinchClient(
    service_plan_id="service_plan_id",
    sms_api_token="api_token",
    sms_region="us"
)
```

> **SMS authentication for new accounts**
>
> Accounts created after the SMS API end-of-sale (`15/04/26`) cannot use
> project-level authentication the SMS API requests return `401 Unauthorized`.
>
> If you encounter this issue, consider the following options:
>
> 1. Use service-plan authentication (`servicePlanId` + `apiToken`)
> 2. Use the Conversation API, which supports project-level authentication.
> 3. Contact your account manager



### Your First Request

Once your client is configured, you can send your first message. The example below uses the Conversation API to send a simple text message over RCS. Replace CONVERSATION_APP_ID with your app ID and RECIPIENT_PHONE_NUMBER with the recipient's phone number:

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
            "channel": "RCS",
            "identity": "RECIPIENT_PHONE_NUMBER",
        }
    ],
)

print(f"Successfully sent message.\n{response}")
```

## Supported APIs


| API Category      | API Name               | Authentication |
|-------------------|------------------------|----------------|
| Messaging         | Conversation API       | OAuth2         |
| Messaging         | SMS                    | OAuth2, APP    |
| Numbers           | Numbers API            | OAuth2         |
| Verification      | Number Lookup API      | OAuth2         |


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
and the [MIGRATION-GUIDE](MIGRATION-GUIDE.md) for instructions on how to update your code when upgrading to a new major version of the SDK.

## License

This project is licensed under the Apache License. 

See the [LICENSE](LICENSE) file for the license text.


## Contact

Developer Experience engineering team: [team-developer-experience@sinch.com](mailto:team-developer-experience@sinch.com)

