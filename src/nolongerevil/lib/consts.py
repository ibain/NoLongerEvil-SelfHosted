"""Global constants and enums."""

from enum import StrEnum

# --- Home Assistant enums ---


class HaMode(StrEnum):
    """Home Assistant HVAC modes."""

    OFF = "off"
    HEAT = "heat"
    COOL = "cool"
    HEAT_COOL = "heat_cool"

    @classmethod
    def all(cls) -> list["HaMode"]:
        """Return all modes as a list."""
        return list(cls)


class HaFanMode(StrEnum):
    """Home Assistant fan modes.

    Include off so HomeKit Fan Active goes inactive when the blower is idle.
    HA HomeKit sets Active=1 whenever HVAC is not off and fan_mode != off;
    publishing auto while idle made the HomeKit fan tile look permanently on.
    """

    OFF = "off"
    AUTO = "auto"
    ON = "on"

    @classmethod
    def all(cls) -> list["HaFanMode"]:
        """Return HomeKit-friendly modes (off/on). Auto kept for command compat."""
        return [cls.OFF, cls.ON]

    @classmethod
    def all_including_auto(cls) -> list["HaFanMode"]:
        """Return all modes including auto."""
        return list(cls)


class HaPreset(StrEnum):
    """Home Assistant preset modes."""

    HOME = "home"
    AWAY = "away"
    ECO = "eco"

    @classmethod
    def all(cls) -> list["HaPreset"]:
        """Return all presets as a list."""
        return list(cls)


class HaAction(StrEnum):
    """Home Assistant HVAC actions."""

    HEATING = "heating"
    COOLING = "cooling"
    FAN = "fan"
    IDLE = "idle"
    OFF = "off"


# --- API enums ---


class ApiMode(StrEnum):
    """API mode values (accepted from external clients)."""

    OFF = "off"
    HEAT = "heat"
    COOL = "cool"
    HEAT_COOL = "heat-cool"
    RANGE = "range"
    AUTO = "auto"
    EMERGENCY = "emergency"


# --- Nest enums ---


class NestMode(StrEnum):
    """Nest thermostat modes (target_temperature_type values)."""

    OFF = "off"
    HEAT = "heat"
    COOL = "cool"
    RANGE = "range"
    EMERGENCY = "emergency"


class NestEcoMode(StrEnum):
    """Nest eco mode values."""

    MANUAL = "manual-eco"
    SCHEDULE = "schedule"


# --- Mappings ---

# API mode to Nest mode mapping
API_MODE_TO_NEST: dict[ApiMode, NestMode] = {
    ApiMode.OFF: NestMode.OFF,
    ApiMode.HEAT: NestMode.HEAT,
    ApiMode.COOL: NestMode.COOL,
    ApiMode.HEAT_COOL: NestMode.RANGE,
    ApiMode.RANGE: NestMode.RANGE,
    ApiMode.AUTO: NestMode.RANGE,
    ApiMode.EMERGENCY: NestMode.EMERGENCY,
}

# Nest mode to HA mode mapping
NEST_MODE_TO_HA: dict[NestMode, HaMode] = {
    NestMode.OFF: HaMode.OFF,
    NestMode.HEAT: HaMode.HEAT,
    NestMode.COOL: HaMode.COOL,
    NestMode.RANGE: HaMode.HEAT_COOL,
    NestMode.EMERGENCY: HaMode.HEAT,  # Emergency heat is a heating mode
}

# HA mode to Nest mode mapping
HA_MODE_TO_NEST: dict[HaMode, NestMode] = {
    HaMode.OFF: NestMode.OFF,
    HaMode.HEAT: NestMode.HEAT,
    HaMode.COOL: NestMode.COOL,
    HaMode.HEAT_COOL: NestMode.RANGE,
}
