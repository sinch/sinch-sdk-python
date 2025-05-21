# Sinch Python SDK

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/sinch/sinch-sdk-python/blob/main/LICENSE)


[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)



Here you'll find documentation related to the Sinch Python SDK, including how to install it, initialize it, and start developing Python code using Sinch services.

To use Sinch services, you'll need a Sinch account and access keys. You can sign up for an account and create access keys at [dashboard.sinch.com](https://dashboard.sinch.com).

For more information on the Sinch APIs on which this SDK is based, refer to the official [developer documentation portal](https://developers.sinch.com).

Further documentation for this SDK, including Python snippets, is available at [sinch.github.io/sinch-sdk-python-docs](https://sinch.github.io/sinch-sdk-python-docs/).


- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Getting started](#getting-started)
- [Logging]()

## Prerequisites

- Python in one of the supported versions - 3.9, 3.10, 3.11, 3.12
- pip
- Sinch account

## Installation

You can install this package by typing:
`pip install sinch`

## Products

The Sinch client provides access to the following Sinch products:
- Numbers API
- SMS API
- Verification API
- Voice API
- Conversation API (beta release)


## Getting started


### Client initialization


To establish a connection with the Sinch backend, you must provide the appropriate credentials based on the API
you intend to use. For security best practices, avoid hardcoding credentials.
Instead, retrieve them from environment variables.

#### Verification and Voice APIs

To initialize the client for the **Verification** and **Voice** APIs, use the following credentials:

```python
from sinch import SinchClient

sinch_client = SinchClient(
    application_key="application_key",
    application_secret="application_secret"
)
```

#### SMS API
For the SMS API in **Australia (AU)**, **Brazil (BR)**, **Canada (CA)**, **the United States (US)**, 
and **the European Union (EU)**,  provide the following parameters:

```python
from sinch import SinchClient

sinch_client = SinchClient(
    service_plan_id="service_plan_id",
    sms_api_token="api_token"
)
```

#### All Other Sinch APIs
For all other Sinch APIs, including SMS in US and EU regions, use the following parameters:

```python
from sinch import SinchClient

sinch_client = SinchClient(
    project_id="project_id",
    key_id="key_id",
    key_secret="key_secret"
)
```

## Logging

Logging configuration for this SDK utilizes following hierarchy:
1. If no configuration was provided via `logger_name` or `logger` configurable, SDK will inherit configuration from the root logger with the `Sinch` prefix.
2. If `logger_name` configurable was provided, SDK will use logger related to that name. For example: `myapp.sinch` will inherit configuration from the `myapp` logger.
3. If `logger` (logger instance) configurable was provided, SDK will use that particular logger for all its logging operations.

If all logging returned by this SDK needs to be disabled, usage of `NullHanlder` provided by the standard `logging` module is advised.  


 
## Sample apps

Usage example of the `numbers` domain:

```python
available_numbers = sinch_client.numbers.available.list(
    region_code="US",
    number_type="LOCAL"
)
```
Returned values are represented as Python `dataclasses`:

```python
ListAvailableNumbersResponse(
    available_numbers=[
        Number(
            phone_number='+17862045855',
            region_code='US',
            type='LOCAL',
            capability=['SMS', 'VOICE'],
            setup_price={'currency_code': 'EUR', 'amount': '0.80'},
            monthly_price={'currency_code': 'EUR', 'amount': '0.80'}
            ...
```

### Handling exceptions

Each API throws a custom, API related exception for an unsuccessful backed call.

Example for Numbers API:

```python
from sinch.domains.numbers.api.v1.exceptions import NumbersException

try:
    nums = sinch_client.numbers.available.list(
        region_code="US",
        number_type="LOCAL"
    )
except NumbersException as err:
    pass
```

For handling all possible exceptions thrown by this SDK use `SinchException` (superclass of all Sinch exceptions) from `sinch.core.exceptions`.


## Custom HTTP client implementation

By default, the HTTP implementation uses the `requests` library.

To use a custom HTTP client, inject your own transport during initialization:
```python
sinch_client = SinchClient(
    key_id="key_id",
    key_secret="key_secret",
    project_id="some_project",
    transport=MyHTTPImplementation
)
```

Custom client has to obey types and methods described by `HTTPTransport` abstract base class:
```python
class HTTPTransport(ABC):
    @abstractmethod
    def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        pass
```

Note: Asynchronous HTTP clients are not supported.
The transport must be a synchronous implementation.

## License

This project is licensed under the Apache License. See the [LICENSE](license.md) file for the license text.
