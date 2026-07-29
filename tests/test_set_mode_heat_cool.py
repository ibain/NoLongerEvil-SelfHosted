"""Tests for control command mode normalization."""

from unittest.mock import MagicMock

import pytest

from nolongerevil.routes.control.command import set_mode


@pytest.mark.asyncio
async def test_set_mode_accepts_ha_heat_cool_underscore() -> None:
    """HA MQTT climate publishes heat_cool; must map to Nest range."""
    state = MagicMock()
    state.get_object.return_value = None
    result = await set_mode(state, "SERIAL", "heat_cool")
    assert result == {"target_temperature_type": "range"}


@pytest.mark.asyncio
async def test_set_mode_accepts_heat_cool_hyphen() -> None:
    state = MagicMock()
    state.get_object.return_value = None
    result = await set_mode(state, "SERIAL", "heat-cool")
    assert result == {"target_temperature_type": "range"}


@pytest.mark.asyncio
async def test_set_mode_accepts_auto_as_range() -> None:
    state = MagicMock()
    state.get_object.return_value = None
    result = await set_mode(state, "SERIAL", "auto")
    assert result == {"target_temperature_type": "range"}
