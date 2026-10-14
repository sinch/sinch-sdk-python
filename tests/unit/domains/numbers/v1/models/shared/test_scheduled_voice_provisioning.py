import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.domains.numbers.models.v1.shared import ScheduledVoiceProvisioning
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_custom import (  # noqa: E501
    ScheduledVoiceProvisioningCustom,
)
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_est import (  # noqa: E501
    ScheduledVoiceProvisioningEST,
)
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_fax import (  # noqa: E501
    ScheduledVoiceProvisioningFAX,
)
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_rtc import (  # noqa: E501
    ScheduledVoiceProvisioningRTC,
)

adapter = TypeAdapter(ScheduledVoiceProvisioning)


@pytest.mark.parametrize(
    "payload, expected_type, expected_fields",
    [
        (
            {"type": "RTC", "status": "WAITING", "appId": "test_app"},
            ScheduledVoiceProvisioningRTC,
            {"app_id": "test_app", "status": "WAITING"},
        ),
        (
            {"type": "EST", "status": "ACTIVE", "trunkId": "test_trunk"},
            ScheduledVoiceProvisioningEST,
            {"trunk_id": "test_trunk", "status": "ACTIVE"},
        ),
        (
            {"type": "FAX", "status": "ACTIVE", "serviceId": "test_service"},
            ScheduledVoiceProvisioningFAX,
            {"service_id": "test_service", "status": "ACTIVE"},
        ),
        (
            {"type": "SOMETHING_NEW", "customField": "custom_value"},
            ScheduledVoiceProvisioningCustom,
            {"type": "SOMETHING_NEW"},
        ),
        (
            {"status": "ACTIVE"},
            ScheduledVoiceProvisioningEST,
            {"status": "ACTIVE"},
        ),
    ],
    ids=["rtc", "est", "fax", "unknown_type", "missing_type"],
)
def test_scheduled_voice_provisioning_resolves_by_type(
    payload, expected_type, expected_fields
):
    """
    Expects each type to resolve to its own variant, an unrecognized type to
    fall back to ScheduledVoiceProvisioningCustom, and a payload without a type
    to resolve by its fields to the first variant it fits.
    """
    with response_parsing_scope():
        provisioning = adapter.validate_python(payload)

    assert type(provisioning) is expected_type
    for name, value in expected_fields.items():
        assert getattr(provisioning, name) == value
