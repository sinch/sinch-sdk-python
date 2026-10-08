from typing import Any, Dict, Iterator, List, Literal, Union, cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.models.v2.svaml.types import (
    GotoMenuCommandDict,
    MenuCommandDict,
    MenuItemDict,
    MenuPromptDict,
    MessageDict,
    NamedMenuItemDict,
    SvamlCommandDict,
)


def _goto_targets(value: Any) -> Iterator[str]:
    """Yields the menu names referenced by ``gotoMenu`` commands in value.

    Nested ``menu`` commands are skipped: they define their own context.
    """
    if isinstance(value, list):
        for item in value:
            yield from _goto_targets(item)
    elif isinstance(value, dict):
        command = value.get("command")
        if command == "menu":
            return
        if command == "gotoMenu":
            yield value["menu_name"]
            return
        for item in value.values():
            yield from _goto_targets(item)


class Menu:
    """Helpers to build the menu SVAML commands."""

    @staticmethod
    def create(name: str, items: List[NamedMenuItemDict]) -> MenuCommandDict:
        """
        Defines a set of named menus and executes them starting from
        ``name``. This is a blocking command — execution waits for the menu
        to complete before proceeding to the next command.

        Each menu item configures prompts, input collection, timeout
        handling, and repeat behavior.

        :param name: Name of the menu to execute first, between 1 and 16
            characters. Must match the name of one of the ``items``.
        :type name: str
        :param items: Menu definitions, built with :meth:`item`. Their names
            must be unique.
        :type items: List[NamedMenuItemDict]
        :returns: The ``menu`` command.
        :rtype: MenuCommandDict
        :raises ValueError: If a menu name is duplicated, or if ``name`` or
            the target of a :meth:`goto` is not one of the ``items``.
        """
        menus: Dict[str, MenuItemDict] = {}
        for item in items:
            item_name = item["name"]
            if item_name in menus:
                raise ValueError(f"Duplicated menu name: '{item_name}'")
            menus[item_name] = cast(
                MenuItemDict,
                {k: v for k, v in item.items() if k != "name"},
            )

        if name not in menus:
            raise ValueError(f"Start menu '{name}' is not defined")
        for target in _goto_targets(list(menus.values())):
            if target not in menus:
                raise ValueError(
                    f"Go-to target menu '{target}' is not defined"
                )

        return {"command": "menu", "start_menu": name, "menus": menus}

    @staticmethod
    def item(
        name: str,
        *,
        prompt: UnsetOr[MenuPromptDict] = UNSET,
        repeat_prompt: UnsetOr[MenuPromptDict] = UNSET,
        input_timeout_duration_seconds: UnsetOr[int] = UNSET,
        repeat_count: UnsetOr[int] = UNSET,
        minimum_input_length: UnsetOr[int] = UNSET,
        maximum_input_length: UnsetOr[int] = UNSET,
        terminating_sequence: UnsetOr[str] = UNSET,
        input_methods: UnsetOr[List[Union[Literal["DTMF"], str]]] = UNSET,
        matches: UnsetOr[Dict[str, List[SvamlCommandDict]]] = UNSET,
        on_failure: UnsetOr[List[SvamlCommandDict]] = UNSET,
    ) -> NamedMenuItemDict:
        r"""
        Defines a single menu step, including prompts, input handling rules,
        input-to-command matches, and failure handling.

        Each collected input is matched against the values in ``matches``.
        If no match succeeds, the ``on_failure`` commands are executed.

        If neither ``matches`` nor ``on_failure`` is defined and the service
        call behavior is ``EVENT_DESTINATION``, an event including the collected input
        is sent to the event destination.

        :param name: Name of the menu, between 1 and 16 characters. Used as
            the start menu in :meth:`create` and as the target of
            :meth:`goto`.
        :type name: str
        :param prompt: Prompt played when this menu starts. This prompt is
            also used as the repeat prompt when ``repeat_prompt`` is not
            defined for the menu.
        :type prompt: UnsetOr[MenuPromptDict]
        :param repeat_prompt: Prompt played when the menu is repeated.
            Repeats occur when input times out or when the provided input
            does not match any menu match item.
        :type repeat_prompt: UnsetOr[MenuPromptDict]
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
        :type matches: UnsetOr[Dict[str, List[SvamlCommandDict]]]
        :param on_failure: SVAML commands executed when the menu fails to
            collect a matching input. This handler runs after the repeat
            limit is reached without any input matching a menu match item.
        :type on_failure: UnsetOr[List[SvamlCommandDict]]
        :returns: The named menu item.
        :rtype: NamedMenuItemDict
        """
        return cast(
            NamedMenuItemDict,
            strip_unset(
                {
                    "name": name,
                    "prompt": prompt,
                    "repeat_prompt": repeat_prompt,
                    "input_timeout_duration_seconds": (
                        input_timeout_duration_seconds
                    ),
                    "repeat_count": repeat_count,
                    "minimum_input_length": minimum_input_length,
                    "maximum_input_length": maximum_input_length,
                    "terminating_sequence": terminating_sequence,
                    "input_methods": input_methods,
                    "matches": matches,
                    "on_fail": on_failure,
                }
            ),
        )

    @staticmethod
    def prompt(
        messages: List[MessageDict],
        *,
        allow_barge_in: UnsetOr[bool] = UNSET,
    ) -> MenuPromptDict:
        """
        Prompt configuration for menu playback, including prompt messages and
        barge-in behavior.

        :param messages: Ordered list of messages to play, between 1 and 10.
        :type messages: List[MessageDict]
        :param allow_barge_in: Controls whether input can interrupt prompt
            playback. When enabled, playback stops as soon as input is
            detected and the input is evaluated immediately if matching
            conditions are met. When disabled, input is still collected
            during playback and evaluated after playback finishes. Defaults
            to ``True``.
        :type allow_barge_in: UnsetOr[bool]
        :returns: The menu prompt.
        :rtype: MenuPromptDict
        """
        return cast(
            MenuPromptDict,
            strip_unset(
                {"messages": messages, "allow_barge_in": allow_barge_in}
            ),
        )

    @staticmethod
    def goto(name: str) -> GotoMenuCommandDict:
        """
        Switches execution to another menu within the current menu context.
        The menu name must be a menu defined in the ``menu`` command. This is
        a blocking command — execution waits for the menu to complete before
        proceeding to the next command.

        This command can only be used within a menu execution context, in
        the ``matches`` or ``on_failure`` of a :meth:`item`.

        :param name: Name of the target menu to execute next, between 1 and
            16 characters. Must match the name of one of the items of the
            menu.
        :type name: str
        :returns: The ``gotoMenu`` command.
        :rtype: GotoMenuCommandDict
        """
        return {"command": "gotoMenu", "menu_name": name}
