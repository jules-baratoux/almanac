from __future__ import annotations

import asyncio
from typing import Any, Callable, Coroutine, Iterable

import flet.testing as ftt
import pytest

import events


class as_completed[T](list[asyncio.Task[T]]):
    def __init__(self, co: Iterable[Coroutine[Any, Any, T]]):
        super().__init__(map(asyncio.create_task, co))

    def __enter__(self):
        return self

    async def __aiter__(self):
        """Asynchronously yields task results as they finish."""
        for future in asyncio.as_completed(self):
            yield await future

    def __exit__(self, exc_type, exc_val, exc_tb):
        for task in self:
            if not task.done():
                task.cancel()

    @staticmethod
    async def item[K, V](key: K, coro: Coroutine[Any, Any, V]) -> tuple[K, V]:
        return key, await coro

    @classmethod
    def map[K](cls,
               function: Callable[[K], Coroutine[Any, Any, T]],
               iterable: Iterable[K]) -> as_completed[tuple[K, T]]:
        return cls(cls.item(key, function(key)) for key in iterable)


@pytest.mark.ui
async def test_any_labels_displayed(flet_app: ftt.FletTestApp):
    """Any label is displayed."""
    tester = flet_app.tester
    await tester.pump_and_settle()

    with as_completed(tester.find_by_text(label.value) for label in events.Labels) as finders:
        async for finder in finders:
            if finder.count > 0:
                return

    pytest.fail("Cannot find any label")
