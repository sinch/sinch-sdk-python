import pytest

from sinch.domains.voice.helpers.v2.svaml import Calls, Menu

SAY = {"type": "SAY", "say": {"text": "Press 1", "voice_name": "Emma"}}


def test_create_expects_items_keyed_by_name():
    """Test that create builds the menus dict keyed by item name."""
    command = Menu.create(
        "main",
        Menu.item("main", matches={"1": [Menu.goto("support")]}),
        Menu.item("support", on_failure=[Calls.hangup()]),
    )

    assert command == {
        "command": "menu",
        "start_menu": "main",
        "menus": {
            "main": {
                "matches": {
                    "1": [{"command": "gotoMenu", "menu_name": "support"}]
                }
            },
            "support": {"on_fail": [{"command": "hangup"}]},
        },
    }


def test_create_expects_duplicated_name_rejected():
    """Test that a duplicated menu name raises ValueError."""
    with pytest.raises(ValueError, match="Duplicated menu name: 'main'"):
        Menu.create("main", Menu.item("main"), Menu.item("main"))


def test_create_expects_undefined_start_menu_rejected():
    """Test that a start menu not in items raises ValueError."""
    with pytest.raises(ValueError, match="Start menu 'other'"):
        Menu.create("other", Menu.item("main"))


def test_create_expects_undefined_goto_target_rejected():
    """Test that a goto to an undefined menu raises ValueError."""
    with pytest.raises(ValueError, match="target menu 'missing'"):
        Menu.create(
            "main", Menu.item("main", on_failure=[Menu.goto("missing")])
        )


def test_create_expects_nested_goto_target_validated():
    """Test that a goto nested in another command's events is validated."""
    item = Menu.item(
        "main",
        matches={
            "1": [Calls.dial("+15551234567", on_hangup=[Menu.goto("x")])]
        },
    )
    with pytest.raises(ValueError, match="target menu 'x'"):
        Menu.create("main", item)


def test_create_expects_goto_in_non_list_sequence_validated():
    """Test that a goto inside a non-list sequence of commands is validated."""
    item = Menu.item("main", matches={"1": (Menu.goto("x"),)})
    with pytest.raises(ValueError, match="target menu 'x'"):
        Menu.create("main", item)


def test_create_expects_nested_menu_context_skipped():
    """Test that goto inside a nested menu is not checked against outer."""
    inner = Menu.create(
        "inner",
        Menu.item("inner", matches={"1": [Menu.goto("inner2")]}),
        Menu.item("inner2"),
    )
    command = Menu.create("main", Menu.item("main", matches={"1": [inner]}))
    assert command["menus"]["main"]["matches"]["1"] == [inner]


def test_item_expects_all_fields():
    """Test that item builds the menu item with all its fields."""
    prompt = Menu.prompt(SAY)
    item = Menu.item(
        "main",
        prompt=prompt,
        repeat_prompt=prompt,
        input_timeout_duration_seconds=10,
        repeat_count=3,
        minimum_input_length=1,
        maximum_input_length=4,
        terminating_sequence="#",
        input_methods=["DTMF"],
        matches={"1": [Calls.hangup()]},
        on_failure=[Calls.hangup()],
    )

    assert item == {
        "name": "main",
        "prompt": {"messages": [SAY]},
        "repeat_prompt": {"messages": [SAY]},
        "input_timeout_duration_seconds": 10,
        "repeat_count": 3,
        "minimum_input_length": 1,
        "maximum_input_length": 4,
        "terminating_sequence": "#",
        "input_methods": ["DTMF"],
        "matches": {"1": [{"command": "hangup"}]},
        "on_fail": [{"command": "hangup"}],
    }


def test_item_expects_optionals_omitted_when_not_provided():
    """Test that omitted optionals are not included."""
    assert Menu.item("main") == {"name": "main"}


def test_prompt_expects_all_fields():
    """Test that prompt builds the prompt with all its fields."""
    assert Menu.prompt(SAY, allow_barge_in=False) == {
        "messages": [SAY],
        "allow_barge_in": False,
    }


def test_prompt_expects_messages_in_order():
    """Test that several messages are kept in the given order."""
    play = {"type": "PLAY", "play": {"url": "https://example.com/a.mp3"}}
    assert Menu.prompt(SAY, play) == {"messages": [SAY, play]}


def test_goto_expects_all_fields():
    """Test that goto builds the command with all its fields."""
    assert Menu.goto("support") == {
        "command": "gotoMenu",
        "menu_name": "support",
    }
