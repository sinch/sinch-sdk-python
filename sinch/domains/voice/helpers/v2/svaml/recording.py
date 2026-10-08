from collections.abc import Sequence
from typing import Union, cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.helpers.v2.svaml.internal.utils import as_commands
from sinch.domains.voice.models.v2.svaml.types import (
    RecordingDestinationType,
    RecordingFormatType,
    RecordingOptionsDict,
    RecordingType,
    StartRecordingCommandDict,
    StopRecordingCommandDict,
    SvamlCommandDict,
    TranscriptionOptionsDict,
)


class Recording:
    """Helpers to build the call recording SVAML commands."""

    @staticmethod
    def options(
        destination: RecordingDestinationType,
        url: str,
        credentials: str,
        *,
        format: UnsetOr[RecordingFormatType] = UNSET,
        recording_type: UnsetOr[RecordingType] = UNSET,
        transcription_options: UnsetOr[TranscriptionOptionsDict] = UNSET,
    ) -> RecordingOptionsDict:
        """
        Recording options to store recordings in a third party storage.

        :param destination: Third party storage to deliver the recording to.

            - ``AWS``: Amazon Web Services S3 bucket.
            - ``GCP``: Google Cloud Platform Storage.
            - ``AZURE``: Microsoft Azure Blob Storage.
        :type destination: RecordingDestinationType
        :param url: Destination URL for the recording. Use ``s3``, ``gs`` or
            ``azure`` as schema for the URL, depending on the destination.
        :type url: str
        :param credentials: Credentials to third party storage.
        :type credentials: str
        :param format: Audio format for this recording. Defaults to ``MP3``.

            - ``MP3``: MPEG Audio Layer III compressed audio format.
            - ``WAV``: Waveform Audio File Format, uncompressed audio.
        :type format: UnsetOr[RecordingFormatType]
        :param recording_type: The type of recording to perform. Defaults to
            ``COMBINED``.

            - ``COMBINED``: Record inbound and outbound voice streams.
            - ``INBOUND``: Record inbound voice stream only.
            - ``OUTBOUND``: Record outbound voice stream only.
        :type recording_type: UnsetOr[RecordingType]
        :param transcription_options: Configuration for automatic
            speech-to-text transcription of the recording: ``is_enabled``
            (if true, the recording will be transcribed to text) and
            ``locale`` (language code in BCP-47 format, defaults to
            ``en-US``).
        :type transcription_options: UnsetOr[TranscriptionOptionsDict]
        :returns: The recording options.
        :rtype: RecordingOptionsDict
        """
        return cast(
            RecordingOptionsDict,
            strip_unset(
                {
                    "destination": destination,
                    "destination_url": url,
                    "credentials": credentials,
                    "format": format,
                    "recording_type": recording_type,
                    "transcription_options": transcription_options,
                }
            ),
        )

    @staticmethod
    def start(
        options: RecordingOptionsDict,
        *,
        name: UnsetOr[str] = UNSET,
        on_finish: UnsetOr[
            Union[SvamlCommandDict, Sequence[SvamlCommandDict]]
        ] = UNSET,
        on_failure: UnsetOr[
            Union[SvamlCommandDict, Sequence[SvamlCommandDict]]
        ] = UNSET,
    ) -> StartRecordingCommandDict:
        r"""
        Starts recording the call. This is a non-blocking command — execution
        continues to the next command in the sequence immediately after
        recording begins.

        :param options: Recording options for this recording, built with
            :meth:`options`.
        :type options: RecordingOptionsDict
        :param name: Identifier for this recording within the session,
            between 1 and 32 characters, matching ``^\S+$``. Must be unique
            across active recordings in the session. Setting the recording
            name is useful for stopping the recording with :meth:`stop`. If
            name is not set, recording can only be stopped when the call is
            disconnected.
        :type name: UnsetOr[str]
        :param on_finish: Commands to execute when the recording is
            successfully stopped. Note that this does not mean that the file
            is delivered to the configured destination yet.
        :type on_finish: UnsetOr[Union[SvamlCommandDict, Sequence[SvamlCommandDict]]]
        :param on_failure: Commands to execute if the recording fails to
            start. If omitted, failures are silently ignored and the call
            flow continues.
        :type on_failure: UnsetOr[Union[SvamlCommandDict, Sequence[SvamlCommandDict]]]
        :returns: The ``startRecording`` command.
        :rtype: StartRecordingCommandDict
        """
        events = strip_unset(
            {
                "on_finish": as_commands(on_finish),
                "on_failure": as_commands(on_failure),
            }
        )
        return cast(
            StartRecordingCommandDict,
            strip_unset(
                {
                    "command": "startRecording",
                    "recording_name": name,
                    "recording_options": options,
                    "events": events if events else UNSET,
                }
            ),
        )

    @staticmethod
    def stop(name: str) -> StopRecordingCommandDict:
        r"""
        Stops a recording previously started by :meth:`start`. This is a
        non-blocking command — execution continues to the next command in
        the sequence immediately after the stop is initiated.

        :param name: Name of the recording to stop, as set by ``name`` in
            :meth:`start`. Between 1 and 32 characters, matching ``^\S+$``.
        :type name: str
        :returns: The ``stopRecording`` command.
        :rtype: StopRecordingCommandDict
        """
        return {"command": "stopRecording", "recording_name": name}
