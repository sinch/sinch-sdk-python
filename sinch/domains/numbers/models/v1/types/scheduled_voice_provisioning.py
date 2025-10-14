from typing import Union
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_est import ScheduledVoiceProvisioningEST
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_fax import ScheduledVoiceProvisioningFAX
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_rtc import ScheduledVoiceProvisioningRTC
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_custom import ScheduledVoiceProvisioningCustom


ScheduledVoiceProvisioning = Union[
    ScheduledVoiceProvisioningEST,
    ScheduledVoiceProvisioningFAX,
    ScheduledVoiceProvisioningRTC,
    ScheduledVoiceProvisioningCustom,
]
