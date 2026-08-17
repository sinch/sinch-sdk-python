from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class HttpRequest:
    headers: dict
    url: str
    http_method: str
    request_body: Optional[Union[str, dict]]
    query_params: dict
    auth: str
