from typing import List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, Unset, UnsetOr
from sinch.domains.voice.api.v2.base.base_voice import BaseVoice
from sinch.domains.voice.api.v2.internal.svaml_endpoints import (
    DescribeSvamlEndpoint,
    ValidateSvamlEndpoint,
)
from sinch.domains.voice.models.v2.svaml.internal.request.describe_svaml_request import (
    DescribeSvamlRequest,
)
from sinch.domains.voice.models.v2.svaml.internal.request.validate_svaml_request import (
    ValidateSvamlRequest,
)
from sinch.domains.voice.models.v2.svaml.response.describe_svaml_response import (
    DescribeSvamlResponse,
)
from sinch.domains.voice.models.v2.svaml.response.validate_svaml_response import (
    ValidateSvamlResponse,
)
from sinch.domains.voice.models.v2.svaml.shared.incoming_call_response_events import (
    IncomingCallResponseEvents,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_input import SvamlInput
from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
    SvamlCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.validation_type import (
    ValidationType,
)


class Svaml(BaseVoice):
    def describe(
        self,
        commands: List[SvamlCommandDict],
        call_name: UnsetOr[Optional[str]] = UNSET,
        on_hangup: UnsetOr[Optional[List[SvamlCommandDict]]] = UNSET,
        **kwargs,
    ) -> DescribeSvamlResponse:
        """
        Describe the call flow from the SVAML payload. This endpoint is useful for understanding the structure and flow of a SVAML payload without executing it. It provides a detailed description of the commands, events, and messages defined in the SVAML.

        :param commands: (required) The ordered list of SVAML commands to describe.
        :type commands: List[SvamlCommandDict]
        :param call_name: (optional) Name of the call.
        :type call_name: UnsetOr[Optional[str]]
        :param on_hangup: (optional) Commands to describe when the call is hung up.
        :type on_hangup: UnsetOr[Optional[List[SvamlCommandDict]]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: A human-readable description of the SVAML call flow.
        :rtype: DescribeSvamlResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        events: UnsetOr[IncomingCallResponseEvents] = UNSET
        if not isinstance(on_hangup, Unset):
            events = IncomingCallResponseEvents(on_hangup=on_hangup)

        request_data = DescribeSvamlRequest(
            svaml=SvamlInput(
                commands=commands,
                **strip_unset({"call_name": call_name, "events": events}),
            ),
            **kwargs,
        )
        return self._request(DescribeSvamlEndpoint, request_data)

    def validate(
        self,
        commands: List[SvamlCommandDict],
        call_name: UnsetOr[Optional[str]] = UNSET,
        on_hangup: UnsetOr[Optional[List[SvamlCommandDict]]] = UNSET,
        validation_type: UnsetOr[Optional[ValidationType]] = UNSET,
        **kwargs,
    ) -> ValidateSvamlResponse:
        """
        Validate a SVAML payload. This endpoint checks the structure and content of the SVAML commands to ensure they conform to the expected schema and rules. It can operate in different validation modes, such as strict or lenient, depending on the requirements.

        :param commands: (required) The ordered list of SVAML commands to validate.
        :type commands: List[SvamlCommandDict]
        :param call_name: (optional) Name of the call.
        :type call_name: UnsetOr[Optional[str]]
        :param on_hangup: (optional) Commands to validate when the call is hung up.
        :type on_hangup: UnsetOr[Optional[List[SvamlCommandDict]]]
        :param validation_type: (optional) Controls how strictly the SVAML payload is validated. If omitted, the server applies the default value `NORMAL`.
        :type validation_type: UnsetOr[Optional[ValidationType]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The result of the SVAML validation.
        :rtype: ValidateSvamlResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        events: UnsetOr[IncomingCallResponseEvents] = UNSET
        if not isinstance(on_hangup, Unset):
            events = IncomingCallResponseEvents(on_hangup=on_hangup)

        svaml = SvamlInput(
            commands=commands,
            **strip_unset({"call_name": call_name, "events": events}),
        )
        request_data = ValidateSvamlRequest(
            svaml=svaml,
            **strip_unset(
                {
                    "validation_type": validation_type,
                }
            ),
            **kwargs,
        )
        return self._request(ValidateSvamlEndpoint, request_data)
