from typing import TypedDict
from typing_extensions import NotRequired
from sinch.domains.conversation.models.v1.credentials.types.basic_auth_credentials_dict import (
    BasicAuthCredentialsDict,
)


class MMSCredentialsDict(TypedDict):
    account_id: str
    api_key: str
    basic_auth: NotRequired[BasicAuthCredentialsDict]
