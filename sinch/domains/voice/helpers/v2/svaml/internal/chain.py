import functools
import inspect
import re
from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from typing_extensions import ParamSpec

from sinch.domains.voice.models.v2.svaml.types import SvamlCommandDict

P = ParamSpec("P")
S = TypeVar("S", bound="CommandsHolder")
Commands = Tuple[SvamlCommandDict, ...]

_RETURNS = re.compile(r":returns:.*?\n(\s*):rtype: [^\n]*", re.DOTALL)
_CREATOR_RETURNS = ":returns: A new creator with the {}.\n\\1:rtype: {}"


class CommandsHolder:
    """Base of the creators and of their open steps, holding the commands.

    A class sets ``_scope`` to name the command its methods complete, and
    ``_check_scope`` to check that command once a method leaves the scope.
    """

    _scope: ClassVar[str] = ""

    def __init__(self) -> None:
        self._commands: Commands = ()

    def _check_scope(self) -> None:
        """Checks the command of the scope, once it is complete."""

    def _leave(self, creator_type: Type["CommandsHolder"]) -> None:
        """Checks the scope if ``creator_type`` is outside of it."""
        if self._scope and creator_type._scope != self._scope:
            self._check_scope()


def append_command(commands: Commands, command: SvamlCommandDict) -> Commands:
    return (*commands, command)


def create(creator_type: Type[S], commands: Commands) -> S:
    creator = creator_type()
    creator._commands = commands
    return creator


class Chain(Generic[P, S]):
    """Descriptor turning a helper into a creator method with its signature.

    Declared as a class attribute of a creator, such as
    ``dial = Chain(Calls.dial, lambda: CommandsSequenceCreator)``. Called on
    a creator, the method calls ``helper`` with the given arguments, places
    its result with ``apply`` and returns a new creator of the type given by
    ``step``. The creator it is called on is left unchanged.

    :param helper: Function building the result, a command or a part of
        one. The method takes its parameters and its docstring.
    :type helper: Callable[P, Any]
    :param step: Callable returning the type of the creator returned by the
        method. A callable because the steps are defined after the creator
        they extend.
    :type step: Callable[[], Type[S]]
    :param apply: Function taking the commands of the creator and the
        result of ``helper``, and returning the commands of the new creator.
        Appends the result as a command by default.
    :type apply: Callable[[Commands, Any], Commands]
    :param returns: What the method does with the result, used to replace
        the ``:returns:`` of the helper in the method docstring.
    :type returns: str
    """

    def __init__(
        self,
        helper: Callable[P, Any],
        step: Callable[[], Type[S]],
        apply: Callable[[Commands, Any], Commands] = append_command,
        returns: str = "command appended",
    ) -> None:
        self._helper = helper
        self._step = step
        self._apply = apply
        self._returns = returns
        self._signature: Optional[inspect.Signature] = None
        self.__doc__ = helper.__doc__

    @overload
    def __get__(self, instance: None, owner: type) -> "Chain[P, S]": ...

    @overload
    def __get__(
        self, instance: CommandsHolder, owner: type
    ) -> Callable[P, S]: ...

    def __get__(
        self, instance: Optional[CommandsHolder], owner: type
    ) -> Union["Chain[P, S]", Callable[P, S]]:
        creator_type = self._prepare()
        if instance is None:
            return self
        helper = self._helper
        apply = self._apply

        @functools.wraps(helper)
        def method(*args: P.args, **kwargs: P.kwargs) -> S:
            instance._leave(creator_type)
            return create(
                creator_type,
                apply(instance._commands, helper(*args, **kwargs)),
            )

        method.__doc__ = self.__doc__
        setattr(method, "__signature__", self._signature)
        return method

    def _prepare(self) -> Type[S]:
        """Resolves the step, and documents it as the returned type."""
        creator_type = self._step()
        if self._signature is None:
            self._signature = inspect.signature(self._helper).replace(
                return_annotation=creator_type
            )
            self.__doc__ = _RETURNS.sub(
                _CREATOR_RETURNS.format(self._returns, creator_type.__name__),
                self._helper.__doc__ or "",
            )
        return creator_type
