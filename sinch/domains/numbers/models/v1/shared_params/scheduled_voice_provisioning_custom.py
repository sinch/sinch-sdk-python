from pydantic import StrictStr
from sinch.domains.numbers.models.v1.internal import BaseModelConfigResponse


class ScheduledVoiceProvisioningCustom(BaseModelConfigResponse):
    type: StrictStr
