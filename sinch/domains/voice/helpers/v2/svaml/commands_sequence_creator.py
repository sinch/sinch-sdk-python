from collections.abc import Sequence
from typing import Callable, List, Union, overload

from sinch.domains.voice.helpers.v2.svaml.amd import Amd
from sinch.domains.voice.helpers.v2.svaml.calls import Calls
from sinch.domains.voice.helpers.v2.svaml.custom_events import CustomEvents
from sinch.domains.voice.helpers.v2.svaml.internal import creator_commands
from sinch.domains.voice.helpers.v2.svaml.internal.chain import (
    Chain,
    CommandsHolder,
    P,
    create,
)
from sinch.domains.voice.helpers.v2.svaml.menu import Menu
from sinch.domains.voice.helpers.v2.svaml.messages import Messages
from sinch.domains.voice.helpers.v2.svaml.recording import Recording
from sinch.domains.voice.models.v2.svaml.types import SvamlCommandDict


def _chain(
    helper: Callable[P, SvamlCommandDict],
) -> "Chain[P, CommandsSequenceCreator]":
    """Creator method appending the command built by ``helper``."""
    return Chain(helper, lambda: CommandsSequenceCreator)


class CommandsSequenceCreator(CommandsHolder, Sequence[SvamlCommandDict]):
    """
    Immutable fluent creator of a sequence of SVAML commands.

    Each method takes the same parameters as the matching helper and returns
    a new creator with the command appended, so a creator can be reused as
    the prefix of several sequences.

    A creator is a sequence of commands, so it can be passed wherever a
    sequence of commands is expected, such as ``commands`` or the ``on_*``
    handlers, without calling :meth:`build`.
    """

    @overload
    def __getitem__(self, index: int) -> SvamlCommandDict: ...

    @overload
    def __getitem__(self, index: slice) -> "CommandsSequenceCreator": ...

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[SvamlCommandDict, "CommandsSequenceCreator"]:
        if isinstance(index, slice):
            return create(CommandsSequenceCreator, self._commands[index])
        return self._commands[index]

    def __len__(self) -> int:
        return len(self._commands)

    def __repr__(self) -> str:
        return f"CommandsSequenceCreator({list(self._commands)!r})"

    def command(self, command: SvamlCommandDict) -> "CommandsSequenceCreator":
        """
        Appends a command, such as one built with a helper or by hand.

        :param command: The command to append.
        :type command: SvamlCommandDict
        :returns: A new creator with the command appended.
        :rtype: CommandsSequenceCreator
        """
        self._leave(CommandsSequenceCreator)
        return create(CommandsSequenceCreator, (*self._commands, command))

    def build(self) -> List[SvamlCommandDict]:
        """
        Returns the commands as a list.

        :returns: The commands, in order.
        :rtype: List[SvamlCommandDict]
        :raises ValueError: If the start menu of a ``menu`` command or the
            target of one of its ``gotoMenu`` commands is not one of its
            menus.
        """
        creator_commands.check_menus(self._commands)
        return list(self._commands)

    answer = _chain(Calls.answer)
    bridge_call = _chain(Calls.bridge_call)
    dial = _chain(Calls.dial)
    hangup = _chain(Calls.hangup)
    pause = _chain(Calls.pause)
    amd = _chain(Amd.activate)
    custom_events = _chain(CustomEvents.trigger)
    messages = Chain(
        creator_commands.messages_command, lambda: OpenMessagesStep
    )
    stop_messages = _chain(Messages.stop)
    text = _chain(creator_commands.text_command)
    play = _chain(creator_commands.play_command)
    recording = _chain(Recording.start)
    stop_recording = _chain(Recording.stop)
    menu = Chain(creator_commands.menu_command, lambda: OpenMenuStep)
    goto_menu = _chain(Menu.goto)


class _MessagesContent:
    """Methods adding a message to the ``messages`` command being built."""

    text = Chain(
        Messages.text,
        lambda: MessagesStep,
        creator_commands.add_message,
        "message added",
    )
    ssml = Chain(
        Messages.ssml,
        lambda: MessagesStep,
        creator_commands.add_message,
        "message added",
    )
    play = Chain(
        Messages.play,
        lambda: MessagesStep,
        creator_commands.add_message,
        "message added",
    )


class OpenMessagesStep(_MessagesContent, CommandsHolder):
    """
    Returned by ``messages``. Not a sequence of commands yet: the command
    needs a first message, added with ``text``, ``ssml`` or ``play``.
    """


class MessagesStep(_MessagesContent, CommandsSequenceCreator):
    """
    Creator whose ``text``, ``ssml`` and ``play`` add a message to the
    ``messages`` command instead of appending a new command.

    Any other method continues the sequence with a new command.
    """


class _MenuScope(CommandsHolder):
    """Checks the references of the ``menu`` command once it is complete."""

    _scope = "menu"

    def _check_scope(self) -> None:
        creator_commands.check_last_menu(self._commands)


class _MenuContent:
    """Method adding a menu to the ``menu`` command being built."""

    item = Chain(
        creator_commands.menu_item,
        lambda: MenuItemStep,
        creator_commands.add_menu_item,
        "menu added",
    )


class OpenMenuStep(_MenuContent, _MenuScope):
    """
    Returned by ``menu``. Not a sequence of commands yet: the command needs
    a first menu, added with ``item``.
    """


class MenuItemStep(_MenuContent, _MenuScope, CommandsSequenceCreator):
    """
    Creator whose ``prompt`` and ``repeat_prompt`` set the prompts of the
    last menu, and whose ``item`` adds another menu to the ``menu`` command.

    Any other method continues the sequence with a new command, once the
    start menu and the ``gotoMenu`` targets of the command are checked.
    """

    prompt = Chain(
        creator_commands.menu_prompt,
        lambda: OpenPromptStep,
        creator_commands.set_prompt("prompt"),
        "prompt set",
    )
    repeat_prompt = Chain(
        creator_commands.menu_prompt,
        lambda: OpenRepeatPromptStep,
        creator_commands.set_prompt("repeat_prompt"),
        "repeat prompt set",
    )


class _PromptContent:
    """Methods adding a message to the prompt being built."""

    text = Chain(
        Messages.text,
        lambda: PromptStep,
        creator_commands.add_prompt_message("prompt"),
        "message added",
    )
    ssml = Chain(
        Messages.ssml,
        lambda: PromptStep,
        creator_commands.add_prompt_message("prompt"),
        "message added",
    )
    play = Chain(
        Messages.play,
        lambda: PromptStep,
        creator_commands.add_prompt_message("prompt"),
        "message added",
    )


class OpenPromptStep(_PromptContent, _MenuScope):
    """
    Returned by ``prompt``. Not a sequence of commands yet: the prompt needs
    a first message, added with ``text``, ``ssml`` or ``play``.
    """


class PromptStep(_PromptContent, MenuItemStep):
    """
    Creator whose ``text``, ``ssml`` and ``play`` add a message to the
    prompt instead of appending a new command.
    """


class _RepeatPromptContent:
    """Methods adding a message to the repeat prompt being built."""

    text = Chain(
        Messages.text,
        lambda: RepeatPromptStep,
        creator_commands.add_prompt_message("repeat_prompt"),
        "message added",
    )
    ssml = Chain(
        Messages.ssml,
        lambda: RepeatPromptStep,
        creator_commands.add_prompt_message("repeat_prompt"),
        "message added",
    )
    play = Chain(
        Messages.play,
        lambda: RepeatPromptStep,
        creator_commands.add_prompt_message("repeat_prompt"),
        "message added",
    )


class OpenRepeatPromptStep(_RepeatPromptContent, _MenuScope):
    """
    Returned by ``repeat_prompt``. Not a sequence of commands yet: the
    prompt needs a first message, added with ``text``, ``ssml`` or ``play``.
    """


class RepeatPromptStep(_RepeatPromptContent, MenuItemStep):
    """
    Creator whose ``text``, ``ssml`` and ``play`` add a message to the
    repeat prompt instead of appending a new command.
    """
