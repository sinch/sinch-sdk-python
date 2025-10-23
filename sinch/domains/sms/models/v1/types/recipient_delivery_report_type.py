from typing import Literal, Union
from pydantic import StrictStr


RecipientDeliveryReportType = Union[
    Literal["recipient_delivery_report_sms", "recipient_delivery_report_mms"],
    StrictStr,
]
