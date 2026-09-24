"""Tests for set_mode input handling."""

from unittest.mock import MagicMock

import pytest

from nolongerevil.routes.control.command import CommandError, set_mode


def state_service() -> MagicMock:
    state = MagicMock()
    state.get_object.return_value = None
    return state


@pytest.mark.parametrize("mode", ["heat_cool", "heat-cool", "range", "auto"])
async def test_heat_cool_aliases_map_to_range(mode: str) -> None:
    result = await set_mode(state_service(), "SERIAL", mode)

    assert result == {"target_temperature_type": "range"}


async def test_unknown_mode_is_rejected() -> None:
    with pytest.raises(CommandError):
        await set_mode(state_service(), "SERIAL", "dry")
