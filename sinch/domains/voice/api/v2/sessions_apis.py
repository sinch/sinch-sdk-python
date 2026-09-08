from sinch.domains.voice.api.v2.base.base_voice import BaseVoice
from sinch.domains.voice.api.v2.internal.sessions_endpoints import (
    GetSessionEndpoint,
)
from sinch.domains.voice.models.v2.sessions.internal.request.session_id_request import (
    SessionIdRequest,
)
from sinch.domains.voice.models.v2.sessions.response.session_response import (
    SessionResponse,
)


class Sessions(BaseVoice):
    def get(self, session_id: str, **kwargs) -> SessionResponse:
        """
        Retrieve detailed information about a specific session, including all associated calls and their current states. Sessions represent the complete interaction lifecycle and can contain multiple related calls.

        :param session_id: (required) The ID of the session.
        :type session_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The session details.
        :rtype: SessionResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice/.
        """
        request_data = SessionIdRequest(session_id=session_id, **kwargs)
        return self._request(GetSessionEndpoint, request_data)
