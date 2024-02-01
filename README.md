<h1 align="center">

   [![Sinch Logo](https://developers.sinch.com/static/logo-07afe977d6d9dcd21b066d1612978e5c.svg)](https://www.sinch.com)

   Python SDK

   [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/sinch/sinch-sdk-python/blob/main/LICENSE)


   [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
   [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
   [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
   [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)


</h1>

# Sinch Python SDK


Here you'll find documentation related to the Sinch Python SDK, including how to install it, initialize it, and start developing Python code using Sinch services.

To use Sinch services, you'll need a Sinch account and access keys. You can sign up for an account and create access keys at [dashboard.sinch.com](https://dashboard.sinch.com).

For more information on the Sinch APIs on which this SDK is based, refer to the official [developer documentation portal](developers.sinch.com).

**This SDK is currently available to selected developers for preview use only. It is being provided for the purpose of collecting feedback, and should not be used in production environments.**

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

## Getting started

### Client initialization


To initialize communication with Sinch backed, credentials obtained from Sinch portal have to be provided to the main client class of this SDK.
It's highly advised to not hardcode those credentials, but to fetch them from environment variables:

```python
from sinch import Client

sinch_client = Client(
    key_id="key_id",
    key_secret="key_secret",
    project_id="some_project",
    application_key="application_key",
    application_secret="application_secret"
)
```

```python
import os
from sinch import Client

sinch_client = Client(
    key_id=os.getenv("KEY_ID"),
    key_secret=os.getenv("KEY_SECRET"),
    project_id=os.getenv("PROJECT_ID"),
    application_key=os.getenv("APPLICATION_KEY"),
    application_secret=os.getenv("APPLICATION_SECRET")
)
```

## Products

Sinch client provides access to the following Sinch products:
- Numbers
- SMS
- Verification
- Conversation API
- Additional products coming soon!

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
from sinch.domains.numbers.exceptions import NumbersException

try:
    nums = sinch_client.numbers.available.list(
        region_code="US",
        number_type="LOCAL"
    )
except NumbersException as err:
    pass
```

For handling all possible exceptions thrown by this SDK use `SinchException` (superclass of all Sinch exceptions) form `sinch.core.exceptions`.


## Custom HTTP client implementation

By default, two HTTP implementations are provided:
- Synchronous using `requests` HTTP library
- Asynchronous using `aiohttp` HTTP library

For creating custom HTTP client code, use either `Client` or `ClientAsync` client and inject your transport during initialisation:
```python
sinch_client = ClientAsync(
    key_id="Spanish",
    key_secret="Inquisition",
    project_id="some_project",
    transport=MyHTTPAsyncImplementation
)
```

Custom client has to obey types and methods described by `HTTPTransport` abstract base class:
```python
class HTTPTransport(ABC):
    @abstractmethod
    def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        pass
```
## License

This project is licensed under the Apache License. See the [LICENSE](license.md) file for the license text.