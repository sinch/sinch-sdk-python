from typing import List, Literal, Union, cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.models.v2.types import (
    BaseCallDestinationDict,
    PhoneDict,
)
from sinch.domains.voice.models.v2.types.call_header_dict import CallHeaderDict
from sinch.domains.voice.models.v2.types.sip_dict import SipDict
from sinch.domains.voice.models.v2.types.sip_from_dict import SipFromDict
from sinch.domains.voice.models.v2.types.stream_dict import (
    StreamDict,
    StreamOptionsDict,
)
from sinch.domains.voice.models.v2.types.voice_name import VoiceName
from sinch.domains.voice.models.v2.types.voice_name_enum import (
    VoiceNameEnum,
)
from sinch.domains.voice.models.v2.types.voice_relay_dict import (
    VoiceRelayDict,
)

_PHONE_PREFIX = "phone:"
_STREAM_PREFIX = "stream:"
_SIP_SCHEMES = ("sip:", "sips:")


class Destination:
    """Helpers to build the ``to`` and ``from_`` endpoints of a call."""

    @staticmethod
    def of(value: str) -> BaseCallDestinationDict:
        """
        Builds a call endpoint from a string, detecting its type from the
        prefix:

        - ``phone:+15551234567`` → phone number on the PSTN, prefix removed.
        - ``sip:user@domain`` / ``sips:user@domain`` → SIP endpoint, URI
          kept as is.
        - ``stream:wss://host/path`` → WebSocket stream endpoint, prefix
          removed.
        - Anything else → phone number, value kept as is.

        The result only contains the fields found in the string and is
        accepted as both ``to`` and ``from_`` of :meth:`Calls.dial`. A stream
        endpoint is only valid as ``to``. Use the dedicated helpers to set
        the optional fields.

        :param value: Endpoint, optionally prefixed with its type.
        :type value: str
        :returns: The phone, SIP or stream endpoint.
        :rtype: BaseCallDestinationDict
        """
        if value.startswith(_SIP_SCHEMES):
            return {"type": "SIP", "sip": {"endpoint": value}}
        if value.startswith(_STREAM_PREFIX):
            endpoint = value[len(_STREAM_PREFIX) :]
            return {"type": "STREAM", "stream": {"endpoint": endpoint}}
        if value.startswith(_PHONE_PREFIX):
            value = value[len(_PHONE_PREFIX) :]
        return Destination.phone(value)

    @staticmethod
    def phone(number: str) -> PhoneDict:
        r"""
        Builds a phone endpoint, which routes the call to a phone number on
        the Public Switched Telephone Network (PSTN). Valid as both ``to``
        and ``from_``.

        :param number: Phone number in E.164 format, between 3 and 16
            characters, matching ``^\+[1-9]\d{1,14}$``.
        :type number: str
        :returns: The phone endpoint.
        :rtype: PhoneDict
        """
        return {"type": "PHONE", "phone": {"number": number}}

    @staticmethod
    def sip(
        endpoint: str,
        *,
        transport: UnsetOr[Union[Literal["UDP", "TCP", "TLS"], str]] = UNSET,
        call_headers: UnsetOr[List[CallHeaderDict]] = UNSET,
    ) -> SipDict:
        """
        Builds a SIP destination, which routes the call to a SIP (Session
        Initiation Protocol) endpoint. Only valid as ``to``; use
        :meth:`sip_from` for ``from_``.

        :param endpoint: SIP URI of the destination endpoint, at most 256
            characters, matching ``^sips?:``. Both ``sip:`` (unencrypted)
            and ``sips:`` (TLS-encrypted) schemes are supported.
        :type endpoint: str
        :param transport: Transport protocol to use for the SIP signalling
            channel. If omitted, the platform selects a default based on the
            URI scheme: ``UDP`` for ``sip:`` and ``TLS`` for ``sips:``.
            Setting this explicitly overrides that default — for example, to
            force ``TCP`` for a ``sip:`` URI or to use ``TLS`` without
            switching to the ``sips:`` scheme.

            - ``UDP``: Connectionless transport. Lowest overhead; suitable
              for most standard SIP deployments.
            - ``TCP``: Connection-oriented transport. More reliable for large
              SIP messages or NAT traversal scenarios.
            - ``TLS``: Encrypted transport. Provides confidentiality and
              integrity for SIP signalling.
        :type transport: UnsetOr[Union[Literal["UDP", "TCP", "TLS"], str]]
        :param call_headers: Custom SIP headers sent in the call setup, at
            most 16.
        :type call_headers: UnsetOr[List[CallHeaderDict]]
        :returns: The SIP destination.
        :rtype: SipDict
        """
        return cast(
            SipDict,
            {
                "type": "SIP",
                "sip": strip_unset(
                    {
                        "endpoint": endpoint,
                        "transport": transport,
                        "call_headers": call_headers,
                    }
                ),
            },
        )

    @staticmethod
    def sip_from(
        endpoint: str, *, display_name: UnsetOr[str] = UNSET
    ) -> SipFromDict:
        """
        Builds a SIP origin, which indicates the call originates from a SIP
        (Session Initiation Protocol) endpoint. Only valid as ``from_``; use
        :meth:`sip` for ``to``.

        :param endpoint: SIP URI of the originating endpoint, at most 192
            characters, matching ``^sips?:``. Both ``sip:`` (unencrypted)
            and ``sips:`` (TLS-encrypted) schemes are supported.
        :type endpoint: str
        :param display_name: Name presented to the called party as the caller
            identity, at most 64 characters. Sent as the display name part of
            the SIP ``From`` header.
        :type display_name: UnsetOr[str]
        :returns: The SIP origin.
        :rtype: SipFromDict
        """
        return cast(
            SipFromDict,
            {
                "type": "SIP",
                "sip": strip_unset(
                    {"endpoint": endpoint, "display_name": display_name}
                ),
            },
        )

    @staticmethod
    def stream(
        endpoint: str,
        *,
        stream_options: UnsetOr[StreamOptionsDict] = UNSET,
        call_headers: UnsetOr[List[CallHeaderDict]] = UNSET,
    ) -> StreamDict:
        """
        Builds a stream destination, which routes the call to a WebSocket
        endpoint for real-time audio processing. Only valid as ``to``.

        :param endpoint: WebSocket URL that accepts the incoming connection,
            using ``ws://`` or ``wss://`` (recommended). It must be reachable
            from the public internet and handle the negotiated stream
            protocol.
        :type endpoint: str
        :param stream_options: Stream protocol options: ``version`` (defaults
            to ``1``), ``codec`` (only ``PCM``, uncompressed raw audio) and
            ``sample_rate`` in Hz (defaults to ``8000``, the PSTN rate; higher
            rates only help on non-PSTN paths and increase bandwidth).
        :type stream_options: UnsetOr[StreamOptionsDict]
        :param call_headers: Custom headers sent in the call setup, at most
            16.
        :type call_headers: UnsetOr[List[CallHeaderDict]]
        :returns: The stream destination.
        :rtype: StreamDict
        """
        return cast(
            StreamDict,
            {
                "type": "STREAM",
                "stream": strip_unset(
                    {
                        "endpoint": endpoint,
                        "stream_options": stream_options,
                        "call_headers": call_headers,
                    }
                ),
            },
        )

    @staticmethod
    def voice_relay(
        endpoint: str,
        tts_voice: Union[VoiceNameEnum, VoiceName],
        stt_language: str,
        *,
        enable_interruptions: UnsetOr[bool] = UNSET,
        call_headers: UnsetOr[List[CallHeaderDict]] = UNSET,
    ) -> VoiceRelayDict:
        """
        Builds a Voice Relay destination, which routes the call through the
        Voice Relay service, enabling real-time speech-to-text (STT) and
        text-to-speech (TTS) over a WebSocket connection to the application
        backend. Only valid as ``to``.

        :param endpoint: URL of the server that accepts the WebSocket
            request.
        :type endpoint: str
        :param tts_voice: Default voice for speech synthesis, used when a
            WebSocket TTS message does not override it. Use
            ``VoiceNameEnum`` to browse voices with their language, gender
            and pricing, or ``VoiceNameByLanguageEnum`` to browse them
            grouped by language.
        :type tts_voice: Union[VoiceNameEnum, VoiceName]
        :param stt_language: BCP-47 language tag used to transcribe the
            inbound audio.
        :type stt_language: str
        :param enable_interruptions: Allows barge-in during TTS playback. When
            ``True`` (the platform default), playback stops as soon as inbound
            speech is detected, unless the content is marked as
            uninterruptible. When ``False``, playback continues, but an
            interruption signal is still sent over the WebSocket.
        :type enable_interruptions: UnsetOr[bool]
        :param call_headers: Custom headers sent in the call setup, at most
            16.
        :type call_headers: UnsetOr[List[CallHeaderDict]]
        :returns: The Voice Relay destination.
        :rtype: VoiceRelayDict
        """
        return cast(
            VoiceRelayDict,
            {
                "type": "VOICE_RELAY",
                "voice_relay": strip_unset(
                    {
                        "endpoint": endpoint,
                        "tts_voice": tts_voice,
                        "stt_language": stt_language,
                        "enable_interruptions": enable_interruptions,
                        "call_headers": call_headers,
                    }
                ),
            },
        )
