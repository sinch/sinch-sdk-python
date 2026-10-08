from collections.abc import Sequence
from typing import cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.models.v2.svaml.types import (
    MessageDict,
    MessagesCommandDict,
    PlayMessageDict,
    SayMessageDict,
    StopMessagesCommandDict,
    SvamlCommandDict,
)


class Messages:
    """Helpers to build the message playback SVAML commands."""

    @staticmethod
    def text(text: str, voice_name: str) -> SayMessageDict:
        """
        A text-to-speech (TTS) message item. The platform synthesizes the
        provided plain text into speech and plays it on the call.

        :param text: The plain text to be synthesized into speech, at most
            600 characters.
        :type text: str
        :param voice_name: The name of the voice to use for text-to-speech
            synthesis.
        :type voice_name: str
        :returns: The ``SAY`` message, in ``TEXT`` format.
        :rtype: SayMessageDict
        """
        return {"type": "SAY", "say": {"text": text, "voice_name": voice_name}}

    @staticmethod
    def ssml(ssml: str, voice_name: str) -> SayMessageDict:
        """
        A text-to-speech (TTS) message item using Speech Synthesis Markup
        Language for advanced text-to-speech control. The platform
        synthesizes the provided SSML document into speech and plays it on
        the call.

        :param ssml: A valid SSML document (``<speak>...</speak>``) to be
            synthesized into speech, at most 600 characters.
        :type ssml: str
        :param voice_name: The name of the voice to use for text-to-speech
            synthesis.
        :type voice_name: str
        :returns: The ``SAY`` message, in ``SSML`` format.
        :rtype: SayMessageDict
        """
        return {
            "type": "SAY",
            "say": {"text": ssml, "voice_name": voice_name, "format": "SSML"},
        }

    @staticmethod
    def play(url: str) -> PlayMessageDict:
        """
        An audio file playback message item. The platform fetches and plays
        the audio file at the provided URL on the call.

        :param url: URL of the media to play.
        :type url: str
        :returns: The ``PLAY`` message.
        :rtype: PlayMessageDict
        """
        return {"type": "PLAY", "play": {"url": url}}

    @staticmethod
    def start(
        message: MessageDict,
        *messages: MessageDict,
        name: UnsetOr[str] = UNSET,
        on_finish: UnsetOr[Sequence[SvamlCommandDict]] = UNSET,
    ) -> MessagesCommandDict:
        r"""
        Plays one or more messages on the call. Multiple messages are played
        sequentially in order.

        This is a non-blocking command — the next command in the sequence
        executes immediately while messages play in parallel. The
        ``on_finish`` event can be used to run a command after all messages
        complete.

        :param message: First message to play, built with :meth:`text`,
            :meth:`ssml` or :meth:`play`.
        :type message: MessageDict
        :param messages: Further messages to play in order, up to 10
            messages in total.
        :type messages: MessageDict
        :param name: Name of the message sequence, between 1 and 32
            characters, matching ``^\S+$``. Must be unique within the current
            call session. Can be referenced by :meth:`stop` to control this
            specific message sequence.
        :type name: UnsetOr[str]
        :param on_finish: SVAML commands to execute when all messages in the
            sequence have finished playing.
        :type on_finish: UnsetOr[Sequence[SvamlCommandDict]]
        :returns: The ``messages`` command.
        :rtype: MessagesCommandDict
        """
        events = strip_unset({"on_finish": on_finish})
        return cast(
            MessagesCommandDict,
            strip_unset(
                {
                    "command": "messages",
                    "messages_name": name,
                    "messages": [message, *messages],
                    "events": events if events else UNSET,
                }
            ),
        )

    @staticmethod
    def stop(name: str) -> StopMessagesCommandDict:
        r"""
        Stops a message sequence started by :meth:`start`. It also cancels
        any messages with the same name that appear in the call session in
        the future.

        This is a non-blocking command.

        :param name: Name of the message sequence to stop, as set by ``name``
            in :meth:`start`. Between 1 and 32 characters, matching
            ``^\S+$``.
        :type name: str
        :returns: The ``stopMessages`` command.
        :rtype: StopMessagesCommandDict
        """
        return {"command": "stopMessages", "messages_name": name}
