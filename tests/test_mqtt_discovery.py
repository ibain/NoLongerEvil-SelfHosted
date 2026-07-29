"""Tests for Home Assistant MQTT discovery helpers."""

from nolongerevil.integrations.mqtt.home_assistant_discovery import (
    build_eco_switch_discovery,
    build_leaf_binary_sensor_discovery,
    get_all_discovery_configs,
)


def test_minimal_discovery_exposes_climate_and_eco_switch_only() -> None:
    configs = get_all_discovery_configs(
        "ABC123",
        {},
        {"target_temperature_type": "heat"},
        "nolongerevil",
        minimal_discovery=True,
    )
    topics = [topic for topic, _payload in configs]
    assert any("/climate/" in topic for topic in topics)
    assert any("/switch/" in topic and "/eco/" in topic for topic in topics)
    assert len(configs) == 2


def test_eco_switch_and_leaf_have_distinct_names() -> None:
    switch = build_eco_switch_discovery("ABC123", "nolongerevil")
    leaf = build_leaf_binary_sensor_discovery("ABC123", "nolongerevil")
    assert switch["name"] != leaf["name"]
    assert switch["unique_id"] != leaf["unique_id"]
    assert "eco_switch" in switch["command_topic"]
    assert leaf.get("command_topic") is None
