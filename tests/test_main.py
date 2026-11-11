from __future__ import annotations

import flet.testing as ftt
import humanize
import pytest

import events


@pytest.mark.ui
async def test_any_labels_displayed(
        flet_app: ftt.FletTestApp,
        labels=tuple(label.value for label in events.Labels)
):
    """Any label is displayed."""
    tester = flet_app.tester
    await tester.pump_and_settle()

    for label in labels:
        finder = await tester.find_by_text(label)
        if finder.count > 0:
            return

    label_values_str = humanize.natural_list(labels)
    pytest.fail(f"Cannot find any label: {label_values_str}")
