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
- [Third-party dependencies](#third-party-dependencies)
- [Examples](#examples)
- [Changelog and Migration](#changelog--migration)
- [Licence](#licence)
- [Contact](#contact)


## Prerequisites

- [Python](https://www.python.org/) in one of the supported versions - 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
- [pip](https://pip.pypa.io/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)

## Installation

You can install this package by typing:

```bash
pip install sinch
```

## Getting Started

To start using the SDK, you need to initialize the main client class with your credentials from your Sinch dashboard. It's highly recommended to not hardcode these credentials and to load them from environment variables instead.



## Products

The Sinch client provides access to the following Sinch products:
- Numbers API
- SMS API
- Conversation API (beta release)


## Getting started


### Client initialization

To establish a connection with the Sinch backend, you must provide credentials based on the API you intend to use.
For security best practices, avoid hardcoding credentials — retrieve them from environment variables instead.

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
afterwards on the `configuration` object, but this must be done **before** the
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
> Accounts created after the SMS API end-of-sale (`<date>`) cannot use
> project auth (OAuth2) for the SMS API requests return `401 Unauthorized`.
>
> If you hit this error, you have three options:
>
> 1. Use service-plan auth (`servicePlanId` + `apiToken`)
> 2. Use the Conversation API, which supports OAuth2.
> 3. Contact your account manager







#### SMS API

The SMS API supports two authentication methods. `sms_region` is required for both and has no default.

**Project auth (OAuth2)**

The SDK automatically exchanges your key ID and key secret for a short-lived OAuth2 token and refreshes it automatically on expiry.
Supported regions: `us`, `eu`, `br`.

In your [Account dashboard](https://dashboard.sinch.com/settings/access-keys), you will find your `projectId` and access keys composed of pairs of `keyId` / `keySecret`.

> **Note:** the `keySecret` is visible only when you create the Access Key. Store it safely and create a new Access Key if you have lost it.

```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="project_id",
    key_id="key_id",
    key_secret="key_secret",
    sms_region="us"
)
```

**Service Plan ID auth (legacy)**

Uses a static bearer token that never expires.
Support all regions: `us`, `eu`, `br`, `ca`, `au`.

In your [Service APIs dashboard](https://dashboard.sinch.com/sms/api/services), you will find your `servicePlanId` and `apiToken` (bearer token).

```python
from sinch import SinchClient

sinch_client = SinchClient(
    service_plan_id="service_plan_id",
    sms_api_token="api_token",
    sms_region="us"
)
```

#### Conversation API - Project auth (OAuth2)

`conversation_region` is required and has no default. 
Supported regions: `us`, `eu`, `br`.

> **Why region matters:** The Conversation API stores and routes data within the selected region for regulatory compliance. Choose the region that matches your data residency requirements.

```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="project_id",
    key_id="key_id",
    key_secret="key_secret",
    conversation_region="eu"
)
```

> **SMS integration note:** If you also use the SMS API, `sms_region` and `conversation_region` **must match**. Mismatched regions will cause delivery failures.

#### Other APIs - Project auth (OAuth2)

These APIs are not regionalized and use project-based auth.

```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="project_id",
    key_id="key_id",
    key_secret="key_secret",
)
```

## Logging

Logging configuration for this SDK utilizes following hierarchy:
1. If no configuration was provided via `logger_name` or `logger` configurable, SDK will inherit configuration from the root logger with the `Sinch` prefix.
2. If `logger_name` configurable was provided, SDK will use logger related to that name. For example: `myapp.sinch` will inherit configuration from the `myapp` logger.
3. If `logger` (logger instance) configurable was provided, SDK will use that particular logger for all its logging operations.

If all logging returned by this SDK needs to be disabled, usage of `NullHandler` provided by the standard `logging` module is advised.


 
## Sample apps

Usage example of the Numbers API via [`VirtualNumbers`](sinch/domains/numbers/virtual_numbers.py) on the client (`sinch_client.numbers`)—`list()` returns your project’s active virtual numbers:

```python
paginator = sinch_client.numbers.list(
    region_code="US",
    number_type="LOCAL",
)
for active_number in paginator.iterator():
    print(active_number)
```

Returned values are [Pydantic](https://docs.pydantic.dev/) model instances (for example [`ActiveNumber`](sinch/domains/numbers/models/v1/response/active_number.py)), including fields such as `phone_number`, `region_code`, `type`, and `capabilities`.

More examples live under [examples/snippets](examples/snippets) on the `main` branch.

### Handling exceptions

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

Note: Asynchronous HTTP clients are not supported.
The transport must be a synchronous implementation.

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for the license text.
