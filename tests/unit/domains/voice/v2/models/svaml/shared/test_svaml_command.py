import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.voice.models.v2.svaml.shared.amd_command import AmdCommand
from sinch.domains.voice.models.v2.svaml.shared.answer_command import (
    AnswerCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.bridge_call_command import (
    BridgeCallCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.dial_command import DialCommand
from sinch.domains.voice.models.v2.svaml.shared.goto_menu_command import (
    GotoMenuCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.menu_command import MenuCommand
from sinch.domains.voice.models.v2.svaml.shared.messages_command import (
    MessagesCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.pause_command import PauseCommand
from sinch.domains.voice.models.v2.svaml.shared.custom_event_command import (
    CustomEventCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.start_recording_command import (
    StartRecordingCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.stop_messages_command import (
    StopMessagesCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.stop_recording_command import (
    StopRecordingCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_command import SvamlCommand

adapter = TypeAdapter(SvamlCommand)

SAY_MESSAGE = {"type": "SAY", "say": {"text": "Hello", "voiceName": "Emma"}}


@pytest.mark.parametrize(
    "payload, expected_model",
    [
        ({"command": "amd"}, AmdCommand),
        (
            {
                "command": "dial",
                "to": {"type": "PHONE", "phone": {"number": "+4673522488"}},
            },
            DialCommand,
        ),
        ({"command": "messages", "messages": [SAY_MESSAGE]}, MessagesCommand),
        (
            {"command": "stopMessages", "messagesName": "my-messages"},
            StopMessagesCommand,
        ),
        (
            {
                "command": "customEvent",
                "webhookName": "my.custom.event",
                "url": "https://example.com/webhook",
            },
            CustomEventCommand,
        ),
        ({"command": "hangup"}, HangupCommand),
        ({"command": "answer"}, AnswerCommand),
        ({"command": "pause", "durationMilliseconds": 1500}, PauseCommand),
        (
            {
                "command": "startRecording",
                "recordingOptions": {
                    "destination": "AWS",
                    "destinationUrl": "s3://bucket/calls",
                    "credentials": "secret",
                },
            },
            StartRecordingCommand,
        ),
        (
            {"command": "stopRecording", "recordingName": "my-recording"},
            StopRecordingCommand,
        ),
        (
            {"command": "bridgeCall", "bridgeName": "my_bridge"},
            BridgeCallCommand,
        ),
        (
            {
                "command": "menu",
                "startMenu": "main",
                "menus": {"main": {"prompt": {"messages": [SAY_MESSAGE]}}},
            },
            MenuCommand,
        ),
        ({"command": "gotoMenu", "menuName": "main"}, GotoMenuCommand),
        (
            {
                "command": "webhook",
                "webhookName": "my.custom.event",
                "url": "https://example.com/webhook",
            },
            ValidationError,
        ),
    ],
)
def test_svaml_command_expects_variant_resolved(payload, expected_model):
    """Test that each command variant of the union is resolved."""
    if issubclass(expected_model, BaseException):
        with pytest.raises(expected_model):
            adapter.validate_python(payload)
    else:
        assert isinstance(adapter.validate_python(payload), expected_model)


def test_svaml_command_expects_validation_error_on_unknown_command():
    """Test that an unknown discriminator value is rejected."""
    with pytest.raises(ValidationError):
        adapter.validate_python({"command": "sing"})


def test_svaml_command_expects_deeply_nested_recursion():
    """Test that command lists nest recursively through event handlers."""
    model = adapter.validate_python(
        {
            "command": "dial",
            "to": {"type": "PHONE", "phone": {"number": "+4673522488"}},
            "events": {
                "onAnswer": [
                    {
                        "command": "amd",
                        "events": {
                            "onMachine": [
                                {
                                    "command": "messages",
                                    "messages": [SAY_MESSAGE],
                                    "events": {
                                        "onFinish": [{"command": "hangup"}]
                                    },
                                }
                            ]
                        },
                    }
                ]
            },
        }
    )

    amd = model.events.on_answer[0]
    messages = amd.events.on_machine[0]
    assert isinstance(amd, AmdCommand)
    assert isinstance(messages, MessagesCommand)
    assert isinstance(messages.events.on_finish[0], HangupCommand)
