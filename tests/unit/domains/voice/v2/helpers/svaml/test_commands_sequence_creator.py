import inspect

import pytest

from sinch.domains.voice.helpers.v2.svaml import (
    Amd,
    Calls,
    CommandsSequenceCreator,
    CustomEvents,
    Menu,
    Messages,
    Recording,
)
from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)

SAY = Messages.text("Hello", "Emma")
PLAY = Messages.play("https://example.com/a.mp3")
SSML = Messages.ssml("<speak>Hi</speak>", "Emma")
OPTIONS = Recording.options("AWS", "s3://bucket/key", "access:secret")


@pytest.mark.parametrize(
    "method, args, kwargs, expected",
    [
        ("answer", (), {}, Calls.answer()),
        ("bridge_call", ("b",), {}, Calls.bridge_call("b")),
        (
            "dial",
            ("+15551234567",),
            {"name": "leg", "on_answer": [Calls.hangup()]},
            Calls.dial("+15551234567", name="leg", on_answer=[Calls.hangup()]),
        ),
        ("hangup", (), {"name": "leg"}, Calls.hangup(name="leg")),
        ("pause", (500,), {}, Calls.pause(500)),
        (
            "amd",
            (),
            {"on_machine": [Calls.hangup()]},
            Amd.activate(on_machine=[Calls.hangup()]),
        ),
        (
            "custom_events",
            ("evt", "https://example.com"),
            {},
            CustomEvents.trigger("evt", "https://example.com"),
        ),
        ("stop_messages", ("greet",), {}, Messages.stop("greet")),
        (
            "recording",
            (OPTIONS,),
            {"name": "rec"},
            Recording.start(OPTIONS, name="rec"),
        ),
        ("stop_recording", ("rec",), {}, Recording.stop("rec")),
        (
            "text",
            ("Hello", "Emma"),
            {"name": "greet", "on_finish": [Calls.hangup()]},
            Messages.start(SAY, name="greet", on_finish=[Calls.hangup()]),
        ),
        (
            "play",
            ("https://example.com/a.mp3",),
            {"name": "music", "on_finish": [Calls.hangup()]},
            Messages.start(
                Messages.play("https://example.com/a.mp3"),
                name="music",
                on_finish=[Calls.hangup()],
            ),
        ),
        ("goto_menu", ("main",), {}, Menu.goto("main")),
    ],
)
def test_method_expects_helper_command_appended(
    method, args, kwargs, expected
):
    """Test that each method appends the command built by its helper."""
    creator = getattr(CommandsSequenceCreator().answer(), method)(
        *args, **kwargs
    )

    assert creator.build() == [Calls.answer(), expected]


def test_command_expects_any_command_appended():
    """Test that command appends a command given as a dict."""
    creator = CommandsSequenceCreator().command({"command": "answer"})

    assert creator.build() == [{"command": "answer"}]


@pytest.mark.parametrize(
    "method, returns, creator_type",
    [
        (
            CommandsSequenceCreator().pause,
            "command appended",
            CommandsSequenceCreator,
        ),
        (
            CommandsSequenceCreator().messages().text,
            "message added",
            type(CommandsSequenceCreator().messages().text("Hello", "Emma")),
        ),
    ],
)
def test_method_expects_creator_return_documented(
    method, returns, creator_type
):
    """Test that methods document and annotate the creator they return."""
    docstring = method.__doc__ or ""

    assert f":returns: A new creator with the {returns}." in docstring
    assert f":rtype: {creator_type.__name__}" in docstring
    assert inspect.signature(method).return_annotation is creator_type


def test_methods_expects_original_creator_unchanged():
    """Test that chaining returns new creators and keeps the original."""
    base = CommandsSequenceCreator().answer()
    first = base.hangup()
    second = base.pause(500)

    assert base.build() == [Calls.answer()]
    assert first.build() == [Calls.answer(), Calls.hangup()]
    assert second.build() == [Calls.answer(), Calls.pause(500)]


def test_build_expects_empty_list_when_no_commands():
    """Test that a creator without commands builds an empty list."""
    assert CommandsSequenceCreator().build() == []


def test_creator_expects_sequence_behavior():
    """Test that the creator supports length, indexing and iteration."""
    creator = CommandsSequenceCreator().answer().hangup()

    assert len(creator) == 2
    assert creator[0] == Calls.answer()
    assert creator[-1] == Calls.hangup()
    assert list(creator) == [Calls.answer(), Calls.hangup()]


def test_slice_expects_new_creator():
    """Test that slicing returns a creator with the selected commands."""
    creator = CommandsSequenceCreator().answer().pause(500).hangup()[1:]

    assert isinstance(creator, CommandsSequenceCreator)
    assert creator.build() == [Calls.pause(500), Calls.hangup()]


def test_messages_expects_chained_messages_added_to_command():
    """Test that text, ssml and play after messages add to that command."""
    creator = (
        CommandsSequenceCreator()
        .messages(name="greet", on_finish=[Calls.hangup()])
        .text("Hello", "Emma")
        .ssml("<speak>Hi</speak>", "Emma")
        .play("https://example.com/a.mp3")
    )

    assert creator.build() == [
        Messages.start(
            SAY, SSML, PLAY, name="greet", on_finish=[Calls.hangup()]
        )
    ]


def test_messages_expects_closed_by_another_command():
    """Test that text after another command appends a new command."""
    creator = (
        CommandsSequenceCreator()
        .messages()
        .text("Hello", "Emma")
        .pause(500)
        .text("Hello", "Emma")
    )

    assert creator.build() == [
        Messages.start(SAY),
        Calls.pause(500),
        Messages.start(SAY),
    ]


def test_messages_expects_original_creator_unchanged():
    """Test that adding a message returns a new creator."""
    base = CommandsSequenceCreator().messages().text("Hello", "Emma")
    extended = base.play("https://example.com/a.mp3")

    assert base.build() == [Messages.start(SAY)]
    assert extended.build() == [Messages.start(SAY, PLAY)]


def test_messages_expects_single_command_handler_wrapped():
    """Test that on_finish given as a single command is sent as a list."""
    creator = (
        CommandsSequenceCreator()
        .messages(on_finish=Calls.hangup())
        .text("Hello", "Emma")
    )

    assert creator.build() == [
        Messages.start(SAY, on_finish=[Calls.hangup()])
    ]


def test_menu_expects_chained_items_built_as_helper():
    """Test that chained menu calls build the same command as the helper."""
    creator = (
        CommandsSequenceCreator()
        .menu("main")
        .item(
            "main",
            repeat_count=2,
            matches={"1": [Menu.goto("support")]},
            on_failure=[Calls.hangup()],
        )
        .prompt(allow_barge_in=False)
        .text("Hello", "Emma")
        .play("https://example.com/a.mp3")
        .repeat_prompt()
        .ssml("<speak>Hi</speak>", "Emma")
        .item("support")
        .prompt()
        .text("Hello", "Emma")
    )

    assert creator.build() == [
        Menu.create(
            "main",
            Menu.item(
                "main",
                repeat_count=2,
                matches={"1": [Menu.goto("support")]},
                on_failure=[Calls.hangup()],
                prompt=Menu.prompt(SAY, PLAY, allow_barge_in=False),
                repeat_prompt=Menu.prompt(SSML),
            ),
            Menu.item("support", prompt=Menu.prompt(SAY)),
        )
    ]


def test_menu_expects_closed_by_another_command():
    """Test that a command after the menu continues the main sequence."""
    creator = (
        CommandsSequenceCreator()
        .menu("main")
        .item("main")
        .prompt()
        .text("Hello", "Emma")
        .hangup()
        .text("Hello", "Emma")
    )

    assert creator.build() == [
        Menu.create("main", Menu.item("main", prompt=Menu.prompt(SAY))),
        Calls.hangup(),
        Messages.start(SAY),
    ]


def test_menu_expects_original_creator_unchanged():
    """Test that completing a menu returns new creators."""
    base = CommandsSequenceCreator().menu("main").item("main")
    extended = base.prompt().text("Hello", "Emma").item("support")

    assert base.build() == [Menu.create("main", Menu.item("main"))]
    assert extended.build() == [
        Menu.create(
            "main",
            Menu.item("main", prompt=Menu.prompt(SAY)),
            Menu.item("support"),
        )
    ]


@pytest.mark.parametrize(
    "call",
    [
        lambda: CommandsSequenceCreator().messages(SAY),
        lambda: CommandsSequenceCreator().menu("main", Menu.item("main")),
        lambda: (
            CommandsSequenceCreator()
            .menu("main")
            .item("main", prompt=Menu.prompt(SAY))
        ),
        lambda: (
            CommandsSequenceCreator()
            .menu("main")
            .item("main", repeat_prompt=Menu.prompt(SAY))
        ),
        lambda: (
            CommandsSequenceCreator().menu("main").item("main").prompt(SAY)
        ),
        lambda: (
            CommandsSequenceCreator()
            .menu("main")
            .item("main")
            .repeat_prompt(SAY)
        ),
    ],
)
def test_content_set_by_chained_calls_expects_argument_rejected(call):
    """Test that content added by chained calls is not taken as argument."""
    with pytest.raises(TypeError):
        call()


@pytest.mark.parametrize(
    "step",
    [
        CommandsSequenceCreator().messages(),
        CommandsSequenceCreator().menu("main"),
        CommandsSequenceCreator().menu("main").item("main").prompt(),
        CommandsSequenceCreator().menu("main").item("main").repeat_prompt(),
    ],
)
def test_open_step_expects_not_a_sequence_of_commands(step):
    """Test that a step missing its first element is not a creator yet."""
    assert not isinstance(step, CommandsSequenceCreator)
    assert not hasattr(step, "build")
    assert not hasattr(step, "hangup")


def test_item_expects_duplicated_name_rejected():
    """Test that a duplicated menu name raises ValueError."""
    creator = CommandsSequenceCreator().menu("main").item("main")

    with pytest.raises(ValueError, match="Duplicated menu name: 'main'"):
        creator.item("main")


def test_menu_expects_undefined_goto_target_rejected_when_left():
    """Test that leaving a menu with an undefined goto target raises."""
    creator = (
        CommandsSequenceCreator()
        .menu("main")
        .item(
            "main",
            matches={"1": CommandsSequenceCreator().goto_menu("missing")},
        )
        .prompt()
        .text("Hello", "Emma")
    )

    with pytest.raises(ValueError, match="target menu 'missing'"):
        creator.hangup()


def test_menu_expects_checked_when_left_by_command():
    """Test that leaving a menu with command checks it too."""
    creator = CommandsSequenceCreator().menu("other").item("main")

    with pytest.raises(ValueError, match="Start menu 'other'"):
        creator.command(Calls.hangup())


def test_menu_expects_goto_to_later_menu_accepted():
    """Test that a goto to a menu added later in the chain is accepted."""
    creator = (
        CommandsSequenceCreator()
        .menu("main")
        .item("main", matches={"1": [Menu.goto("support")]})
        .item("support", matches={"9": [Menu.goto("main")]})
        .hangup()
    )

    assert len(creator) == 2


def test_build_expects_last_menu_checked():
    """Test that build checks a menu that no other command has left."""
    creator = CommandsSequenceCreator().menu("other").item("main")

    with pytest.raises(ValueError, match="Start menu 'other'"):
        creator.build()


def test_build_expects_menu_nested_in_handler_checked():
    """Test that build checks a menu ending a creator given as handler."""
    nested = (
        CommandsSequenceCreator()
        .menu("main")
        .item("main", on_failure=[Menu.goto("missing")])
    )
    creator = CommandsSequenceCreator().dial("+15551234567", on_answer=nested)

    with pytest.raises(ValueError, match="target menu 'missing'"):
        creator.build()
