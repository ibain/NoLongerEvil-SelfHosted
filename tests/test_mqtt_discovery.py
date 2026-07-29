"""Tests for Home Assistant MQTT discovery helpers."""

from nolongerevil.integrations.mqtt.home_assistant_discovery import get_all_discovery_configs


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
