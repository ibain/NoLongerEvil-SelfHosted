"""Device capability helpers shared across control API and MQTT."""

from typing import Any


def device_has_fan(
    shared_values: dict[str, Any],
    device_values: dict[str, Any] | None = None,
) -> bool:
    """Return True when Nest can control/report a fan.

    Prefer explicit has_fan flags. Also treat fan timer / blower fields as
    evidence — some devices omit or clear has_fan but still expose fan
    controls, which left HomeKit climate without a nested fan service.
    """
    dv = device_values or {}
    if shared_values.get("has_fan") is True or dv.get("has_fan") is True:
        return True
    if (
        "fan_timer_timeout" in dv
        or "fan_control_state" in dv
        or "fan_timer_speed" in dv
        or "hvac_fan_state" in shared_values
    ):
        return True
    if shared_values.get("has_fan") is False or dv.get("has_fan") is False:
        return False
    # Default on for heat/cool thermostats so HomeKit can nest fan controls.
    return True
