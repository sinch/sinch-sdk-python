from typing import TypedDict
from typing_extensions import NotRequired


class AppleBusinessChatCredentialsDict(TypedDict):
    business_chat_account_id: str
    merchant_id: NotRequired[str]
    apple_pay_certificate_reference: NotRequired[str]
    apple_pay_certificate_password: NotRequired[str]
