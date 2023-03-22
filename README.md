<h1 align="center">

   [![Sinch Logo](https://cdn.liveagent.com/app/uploads/2021/06/sinch-logo.png)](https://www.sinch.com)

   Python SDK

   [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/sinch/sinch-sdk-python/blob/main/LICENSE)

   [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
   [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
   [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)

   [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
   [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
   [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
   [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

</h1>

## Welcome to Sinch's Python SDK.

Here you'll find documentation to start developing Python code using Sinch services. 

To use this SDK you'll need a Sinch account and API keys. Please sign up at [sinch.com](https://sinch.com)

For more in depth version of the Sinch APIs, please refer to the official developer portal - [developers.sinch.com](https://developers.sinch.com/)

**This SDK is currently available to select developers for preview use only. It is being provided for the purpose of collecting feedback, and should not be used in production environments.**

* [Installation](#installation)
* [Getting started](#getting-started)
* [Logging](#logging)
* [Custom HTTP client implementation](#custom-http-client-implementation)
***


## Installation

You can install this package to your virtual environment or to your global Python installation by cloning this repo and typing:
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
    project_id="some_project"
)
```

```python
import os
from sinch import Client

sinch_client = Client(
    key_id=os.getenv("KEY_ID"),
    key_secret=os.getenv("KEY_SECRET"),
    project_id=os.getenv("PROJECT_ID")
)
```


### Domains

Each product from Sinch portfolio is considered and coded as a separate `domain`.
Domain contains data structures specific to that service, that can be also used by the developer.

Abstract directory structure of the `domain`:
```
├── domain_name
│   ├── __init__.py (public interface of the domain)
│   ├── endpoints (directory with endpoint definitions)
│   ├── models (direcotry with data models definitions)
│   ├── enums.py (enums that can be helpful for a developer; e.g. SinchNumberType)
│   ├── exceptions.py (exceptions spefific for a particular domain; e.g. NumbersException)
│
```

Sinch client provides access to the following Sinch product domains:

- Numbers
- Conversation API
- SMS


Usage example of the `numbers` domain:

```python
from sinch.domains.numbers.enums import NumberType

available_numbers = sinch_client.numbers.available.list(
    region_code="US",
    number_type=NumberType.LOCAL.value,
    project_id="Shrubbery"
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

Each domain throws a `DomainException` exception for an unsuccessful backed call.

Example for Numbers Domain:

```python
from sinch.domains.numbers.exceptions import NumbersException

try:
    nums = sinch_client.numbers.available.list(
        region_code="US",
        number_type="LOCAL",
        project_id="project"
    )
except NumbersException as err:
    pass
```

For handling all possible exceptions thrown by this SDK use `SinchException` (superclass of all Sinch exceptions) form `sinch.core.exceptions`.


## Logging

Logging configuration for this SDK utilizes following hierarchy:
1. If no configuration was provided via `logger_name` or `logger` configurable, SDK will inherit configuration from the root logger with the `Sinch` prefix.
2. If `logger_name` configurable was provided, SDK will use logger related to that name. For example: `myapp.sinch` will inherit configuration from the `myapp` logger.
3. If `logger` (logger instance) configurable was provided, SDK will use that particular logger for all its logging operations.

If all logging returned by this SDK needs to be disabled, usage of `NullHanlder` provided by the standard `logging` module is advised.  


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
