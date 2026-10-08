from collections.abc import Mapping, Sequence
from typing import Any, Callable, Dict, List, Literal, Union, cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.helpers.v2.svaml.internal.chain import Commands
from sinch.domains.voice.helpers.v2.svaml.menu import Menu, _check_references
from sinch.domains.voice.helpers.v2.svaml.messages import Messages
from sinch.domains.voice.models.v2.svaml.types import (
    MenuCommandDict,
    MenuPromptDict,
    MessageDict,
    MessagesCommandDict,
    NamedMenuItemDict,
    SvamlCommandDict,
)


def messages_command(
    *,
    name: UnsetOr[str] = UNSET,
    on_finish: UnsetOr[Sequence[SvamlCommandDict]] = UNSET,
) -> MessagesCommandDict:
    r"""
    Plays one or more messages on the call, sequentially in order. The
    messages are added right after with ``text``, ``ssml`` and ``play``,
    which add to this command until another method is called. Between 1 and
    10 messages are required.

    This is a non-blocking command — the next command in the sequence
    executes immediately while messages play in parallel.

    :param name: Name of the message sequence, between 1 and 32
        characters, matching ``^\S+$``. Must be unique within the current
        call session. Can be referenced by :meth:`stop_messages` to control
        this specific message sequence.
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
                "messages": [],
                "events": events if events else UNSET,
            }
        ),
    )


def text_command(
    text: str,
    voice_name: str,
    *,
    name: UnsetOr[str] = UNSET,
    on_finish: UnsetOr[Sequence[SvamlCommandDict]] = UNSET,
) -> MessagesCommandDict:
    r"""
    Plays a single text-to-speech message on the call. Shortcut for
    :meth:`messages` with one :meth:`Messages.text` message.

    :param text: The plain text to be synthesized into speech, at most
        600 characters.
    :type text: str
    :param voice_name: The name of the voice to use for text-to-speech
        synthesis.
    :type voice_name: str
    :param name: Name of the message sequence, between 1 and 32
        characters, matching ``^\S+$``. Must be unique within the current
        call session. Can be referenced by :meth:`stop_messages` to control
        this specific message sequence.
    :type name: UnsetOr[str]
    :param on_finish: SVAML commands to execute when the message has
        finished playing.
    :type on_finish: UnsetOr[Sequence[SvamlCommandDict]]
    :returns: The ``messages`` command.
    :rtype: MessagesCommandDict
    """
    return Messages.start(
        Messages.text(text, voice_name), name=name, on_finish=on_finish
    )


def play_command(
    url: str,
    *,
    name: UnsetOr[str] = UNSET,
    on_finish: UnsetOr[Sequence[SvamlCommandDict]] = UNSET,
) -> MessagesCommandDict:
    r"""
    Plays a single audio file on the call. Shortcut for :meth:`messages`
    with one :meth:`Messages.play` message.

    :param url: URL of the media to play.
    :type url: str
    :param name: Name of the message sequence, between 1 and 32
        characters, matching ``^\S+$``. Must be unique within the current
        call session. Can be referenced by :meth:`stop_messages` to control
        this specific message sequence.
    :type name: UnsetOr[str]
    :param on_finish: SVAML commands to execute when the message has
        finished playing.
    :type on_finish: UnsetOr[Sequence[SvamlCommandDict]]
    :returns: The ``messages`` command.
    :rtype: MessagesCommandDict
    """
    return Messages.start(Messages.play(url), name=name, on_finish=on_finish)


def menu_command(name: str) -> MenuCommandDict:
    """
    Defines a set of named menus and executes them starting from ``name``.
    The menus are added right after with ``item``. At least one menu is
    required.

    This is a blocking command — execution waits for the menu to complete
    before proceeding to the next command.

    :param name: Name of the menu to execute first, between 1 and 16
        characters. Must match the name of one of the menus.
    :type name: str
    :returns: The ``menu`` command.
    :rtype: MenuCommandDict
    """
    return {"command": "menu", "start_menu": name, "menus": {}}


def menu_item(
    name: str,
    *,
    input_timeout_duration_seconds: UnsetOr[int] = UNSET,
    repeat_count: UnsetOr[int] = UNSET,
    minimum_input_length: UnsetOr[int] = UNSET,
    maximum_input_length: UnsetOr[int] = UNSET,
    terminating_sequence: UnsetOr[str] = UNSET,
    input_methods: UnsetOr[List[Union[Literal["DTMF"], str]]] = UNSET,
    matches: UnsetOr[Mapping[str, Sequence[SvamlCommandDict]]] = UNSET,
    on_failure: UnsetOr[Sequence[SvamlCommandDict]] = UNSET,
) -> NamedMenuItemDict:
    r"""
    Defines a single menu step, including input handling rules,
    input-to-command matches, and failure handling. Its prompts are set
    right after with ``prompt`` and ``repeat_prompt``.

    Each collected input is matched against the values in ``matches``.
    If no match succeeds, the ``on_failure`` commands are executed.

    If neither ``matches`` nor ``on_failure`` is defined and the service
    call behavior is ``EVENT_DESTINATION``, an event including the collected
    input is sent to the event destination.

    :param name: Name of the menu, between 1 and 16 characters. Used as
        the start menu in :meth:`menu` and as the target of
        :meth:`goto_menu`. Menu names must be unique.
    :type name: str
    :param input_timeout_duration_seconds: Maximum number of seconds to
        wait for user input before the input attempt times out, between
        1 and 60. Defaults to 5.
    :type input_timeout_duration_seconds: UnsetOr[int]
    :param repeat_count: Maximum number of times the menu is repeated,
        between 0 and 10. A repeat occurs when input times out or when
        the provided input does not match any menu match item. Defaults
        to 2.
    :type repeat_count: UnsetOr[int]
    :param minimum_input_length: Minimum number of input characters
        required before the menu evaluates the collected input, between
        1 and 100. Defaults to 1.
    :type minimum_input_length: UnsetOr[int]
    :param maximum_input_length: Maximum number of input characters that
        triggers the menu to evaluate the collected input, between 1 and
        100. Defaults to 1.
    :type maximum_input_length: UnsetOr[int]
    :param terminating_sequence: Character sequence that signals the end
        of input and triggers immediate evaluation, at most 10
        characters, matching ``^[0-9*#]+$``. Useful when variable-length
        input is allowed and shorter valid options should be submitted
        without waiting for timeout or maximum length. The terminating
        sequence value is included in the evaluated input.
    :type terminating_sequence: UnsetOr[str]
    :param input_methods: Input methods accepted for this menu when
        collecting user input. Defaults to ``["DTMF"]``.

        - ``DTMF``: Collect input from keypad tones (Dual-Tone
          Multi-Frequency).
    :type input_methods: UnsetOr[List[Union[Literal["DTMF"], str]]]
    :param matches: Items matched against the collected input, at most
        50. Each key is a literal or a regular expression string, between
        1 and 256 characters, and its value is the SVAML commands to
        execute. Keys are evaluated sequentially in the order defined;
        the first key that matches the input triggers its commands. Use
        ``\*`` to match the DTMF star tone (``*``).
    :type matches: UnsetOr[Mapping[str, Sequence[SvamlCommandDict]]]
    :param on_failure: SVAML commands executed when the menu fails to
        collect a matching input. This handler runs after the repeat
        limit is reached without any input matching a menu match item.
    :type on_failure: UnsetOr[Sequence[SvamlCommandDict]]
    :returns: The named menu item.
    :rtype: NamedMenuItemDict
    :raises ValueError: If the menu name is duplicated.
    """
    return Menu.item(
        name,
        input_timeout_duration_seconds=input_timeout_duration_seconds,
        repeat_count=repeat_count,
        minimum_input_length=minimum_input_length,
        maximum_input_length=maximum_input_length,
        terminating_sequence=terminating_sequence,
        input_methods=input_methods,
        matches=matches,
        on_failure=on_failure,
    )


def menu_prompt(*, allow_barge_in: UnsetOr[bool] = UNSET) -> MenuPromptDict:
    """
    Sets a prompt of the menu: the one played when the menu starts
    (``prompt``), also used when the menu is repeated unless the one for
    repeats (``repeat_prompt``) is set. The messages are added right after
    with ``text``, ``ssml`` and ``play``. Between 1 and 10 messages are
    required.

    :param allow_barge_in: Controls whether input can interrupt prompt
        playback. When enabled, playback stops as soon as input is detected
        and the input is evaluated immediately if matching conditions are
        met. When disabled, input is still collected during playback and
        evaluated after playback finishes. Defaults to ``True``.
    :type allow_barge_in: UnsetOr[bool]
    :returns: The menu prompt.
    :rtype: MenuPromptDict
    """
    return cast(
        MenuPromptDict,
        strip_unset({"messages": [], "allow_barge_in": allow_barge_in}),
    )


def add_message(commands: Commands, message: MessageDict) -> Commands:
    """Adds a message to the ``messages`` command at the end of commands."""
    *previous, last = commands
    command = cast(Dict[str, Any], last)
    messages = [*command["messages"], message]
    updated = cast(SvamlCommandDict, {**command, "messages": messages})
    return (*previous, updated)


def add_menu_item(commands: Commands, item: NamedMenuItemDict) -> Commands:
    """Adds a menu to the ``menu`` command at the end of commands."""
    *previous, last = commands
    command = cast(Dict[str, Any], last)
    name = item["name"]
    if name in command["menus"]:
        raise ValueError(f"Duplicated menu name: '{name}'")
    menu = {key: value for key, value in item.items() if key != "name"}
    updated = {**command, "menus": {**command["menus"], name: menu}}
    return (*previous, cast(SvamlCommandDict, updated))


def _update_last_menu_item(
    commands: Commands, update: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> Commands:
    """Updates the last menu of the ``menu`` command at the end of commands."""
    *previous, last = commands
    command = cast(Dict[str, Any], last)
    name = next(reversed(command["menus"]))
    menus = {**command["menus"], name: update(command["menus"][name])}
    updated = cast(SvamlCommandDict, {**command, "menus": menus})
    return (*previous, updated)


def set_prompt(key: str) -> Callable[[Commands, MenuPromptDict], Commands]:
    """Sets the prompt as ``key`` in the last menu of the ``menu`` command."""

    def apply(commands: Commands, prompt: MenuPromptDict) -> Commands:
        return _update_last_menu_item(
            commands, lambda item: {**item, key: prompt}
        )

    return apply


def add_prompt_message(
    key: str,
) -> Callable[[Commands, MessageDict], Commands]:
    """Adds a message to the ``key`` prompt of the last menu."""

    def apply(commands: Commands, message: MessageDict) -> Commands:
        def update(item: Dict[str, Any]) -> Dict[str, Any]:
            messages = [*item[key]["messages"], message]
            return {**item, key: {**item[key], "messages": messages}}

        return _update_last_menu_item(commands, update)

    return apply


def check_last_menu(commands: Commands) -> None:
    """Checks the references of the ``menu`` command at the end of commands.

    :raises ValueError: If its start menu or the target of a ``gotoMenu`` is
        not one of its menus.
    """
    command = cast(Dict[str, Any], commands[-1])
    _check_references(command["start_menu"], command["menus"])


def check_menus(value: Any) -> None:
    """Checks the references of every ``menu`` command in value, including
    the ones nested in handlers.

    :raises ValueError: If a start menu or the target of a ``gotoMenu`` is
        not one of the menus of its ``menu`` command.
    """
    if isinstance(value, Mapping):
        if value.get("command") == "menu":
            _check_references(value["start_menu"], value["menus"])
        for item in value.values():
            check_menus(item)
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for item in value:
            check_menus(item)
