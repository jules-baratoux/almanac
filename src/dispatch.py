import functools
import inspect
import typing
from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, Callable, Mapping, Sequence, cast
from warnings import filterwarnings

from beartype.bite import infer_hint
from beartype.door import is_bearable
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

filterwarnings(action="ignore", category=BeartypeDecorHintPep585DeprecationWarning)


def get_annotation(value) -> str:
    """
    Infer the annotation of ``value``.

    >>> get_annotation("")
    'str'

    >>> get_annotation(0)
    'int'

    >>> get_annotation(3.14)
    'float'

    >>> get_annotation(["a", "b"])
    'list[str]'

    >>> get_annotation({"x": 1})
    'dict[str, int]'
    """
    hint = infer_hint(value)
    if isinstance(hint, type):
        return hint.__name__  # str, int, list, …
    return repr(hint)  # list[str], dict[str, int], …


def yield_arguments(*args, **kwargs):
    for arg in args:
        yield get_annotation(arg)
    for kw, arg in kwargs.items():
        yield f"{kw}: {get_annotation(arg)}"


class Overload:
    def __init__(self, func: Callable):
        functools.update_wrapper(self, func)
        self.__func__ = func
        self.signature = inspect.signature(func)
        self.hints = typing.get_type_hints(func)
        self.hints.pop("return", None)

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)

    def match(self, arguments: Mapping[str, Any]) -> bool:
        for name, hint in self.hints.items():
            parameter = self.signature.parameters[name]
            argument = arguments[name]

            if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
                if not all(is_bearable(item, hint) for item in argument):
                    return False
            elif parameter.kind is inspect.Parameter.VAR_KEYWORD:
                if not all(is_bearable(item, hint) for item in argument.values()):
                    return False
            elif not is_bearable(argument, hint):
                return False

        return True

    def __repr__(self):
        return f"{Overload.__qualname__}({self.__func__!r})"


class Dispatcher[**P, R](ABC):

    def __init__(self, wrapped: Callable[P, R]):
        self.__wrapped__ = wrapped
        functools.update_wrapper(self, wrapped)

    @abstractmethod
    def indirect(self, func, *args, **kwargs):
        """
        See UnboundDispatcher.indirect and BoundDispatcher.indirect.
        """

    @cached_property
    def overloads(self) -> Sequence[Overload]:
        return cast(Sequence[Overload], typing.get_overloads(self.__wrapped__))

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        for overload in self.overloads:

            try:
                bound = self.indirect(overload.signature.bind, *args, **kwargs)
            except TypeError:
                continue

            # Fill in missing optional defaults so match() can see them.
            bound.apply_defaults()

            if overload.match(bound.arguments):
                return self.indirect(overload, *args, **kwargs)

        name = self.__wrapped__.__qualname__
        arguments = ", ".join(yield_arguments(*args, **kwargs))
        raise TypeError(f"{name}({arguments}) has no matching overload")


class UnboundDispatcher(Dispatcher):

    def __get__(self, obj, objtype=None):
        # Used when decorating a method.
        if obj is None:
            return self
        else:
            bound = BoundDispatcher(self.__wrapped__, obj, self)

            # Cache the bound dispatcher on the instance to increase attribute access performance.
            obj.__dict__[self.__name__] = bound

            return bound

    @staticmethod
    def indirect(func, *args, **kwargs):
        """
        Mimic FunctionType by calling ``func(*args, **kwargs)``.
        """
        return func(*args, **kwargs)


class BoundDispatcher(Dispatcher):
    def __init__(self, wrapped, instance, unbound: UnboundDispatcher):
        super().__init__(wrapped)
        self.__func__ = unbound
        self.__self__ = instance

    def indirect(self, func, *args, **kwargs):
        """
        Mimic MethodType by calling ``func(__self__, *args, **kwargs)``.
        """
        return func(self.__self__, *args, **kwargs)


def overload(func):
    # noinspection PyTypeChecker
    """Dispatch generic function decorator.

    Apply ``@overload`` to multiple definitions of the same method to register
    each as an overload. When the method is called on an instance, the first
    overload with a signature matching the supplied arguments is invoked.

    If no overload matches, a :exc:`TypeError` is raised.

    .. code-block:: python

        class Vector:

            @overload
            def __init__(self, x: float, y: float):
                self.x, self.y = x, y

            @overload
            def __init__(self, coords: tuple[float, float]):
                self.x, self.y = coords

        Vector(1.0, 2.0)       # dispatches to first overload
        Vector((1.0, 2.0))     # dispatches to second overload
        Vector("oops")         # TypeError: Vector.__init__(str) has no matching overload

    .. note::

        Overload order matters: the first overload with a signature that can be
        bound and matching argument type hints is used.

    """

    is_static = isinstance(func, staticmethod)
    is_class = isinstance(func, classmethod)
    wrapped = func.__func__ if (is_static or is_class) else func

    wrapper = Overload(wrapped)
    typing.overload(wrapper)

    dispatcher = UnboundDispatcher(wrapped)
    if is_static:
        return staticmethod(dispatcher)
    elif is_class:
        return classmethod(dispatcher)
    else:
        return dispatcher


def test_simple_overload():
    from pytest import raises

    class Vector:

        @overload
        def __init__(self, x: float, y: float):
            self.called_with = lambda *args: args == (x, y)

        @overload
        def __init__(self, coords: tuple[float, float]):
            self.called_with = lambda *args: args == (coords,)

    assert Vector(1.0, 2.0).called_with(1.0, 2.0)
    assert Vector((1.0, 2.0)).called_with((1.0, 2.0))
    with raises(TypeError):
        Vector("oops")


def test_overload_match_variadic_positional():
    from enum import Enum

    class Label(Enum):
        CHINA = "China"
        FRANCE = "France"

    def example(*labels: Label):
        pass

    overloaded = Overload(example)

    bound = overloaded.signature.bind(Label.CHINA)
    assert overloaded.match(bound.arguments)

    bound = overloaded.signature.bind(Label.CHINA, Label.FRANCE)
    assert overloaded.match(bound.arguments)

    bound = overloaded.signature.bind("China")
    assert not overloaded.match(bound.arguments)


__all__ = "overload",
