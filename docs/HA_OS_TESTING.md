# HA OS Testing — Forked NLE Add-on

**Supported Nest → Apple Home path (this setup):** NLE MQTT add-on → Home Assistant → HA HomeKit Bridge + [`ha-homekit-nest-fan`](https://github.com/ibain/ha-homekit-nest-fan). Do **not** use Homebridge for Nest.

Requires NLE Self-Hosted / add-on **0.0.17+** (policy-only `fan_mode`, eco switch, accurate `fan_running`).

## Fork repos

- https://github.com/ibain/NoLongerEvil-SelfHosted (`fix/eco-mode-control`)
- https://github.com/ibain/NoLongerEvil-HomeAssistant (`fix/eco-mode-control`)
- https://github.com/ibain/ha-homekit-nest-fan (HomeKit nested fan patch)

## Install forked add-on

1. HA → **Settings → Add-ons → Add-on Store → Repositories**
2. Add: `https://github.com/ibain/NoLongerEvil-HomeAssistant`
3. Install **NoLongerEvil HomeAssistant** from your fork (stop official add-on first)
4. Set `api_origin` to `http://<HA-LAN-IP>:9543`
5. Enable **mqtt_minimal_discovery** in add-on options (or set `MQTT_MINIMAL_DISCOVERY=true`) to expose only `climate.*` + `switch.*_eco`
6. Restart Mosquitto + forked add-on
7. **Settings → Devices & Services → MQTT → Configure** → reload if entities stale

## Install ha-homekit-nest-fan

1. Copy `custom_components/ha_homekit_nest_fan` into `/config/custom_components/`  
   (or HACS custom repo: `https://github.com/ibain/ha-homekit-nest-fan`)
2. Restart HA → **Add Integration → “HomeKit Nest FanV2 Fix”**
3. Reload **HomeKit Bridge** so thermostat accessories rebuild with the fan patch

## HomeKit Bridge filter

Expose:

- `climate.nest_<serial>`
- `switch.nest_<serial>_eco`

Exclude:

- `binary_sensor.nest_*_occupancy`
- `binary_sensor.nest_*_fan` (optional if you only want nested fan via `ha-homekit-nest-fan`)
- `binary_sensor.nest_*_leaf`
- diagnostic sensors (battery, rssi, etc.)

Use **one** bridge only: HA HomeKit Bridge. Do not pair Nest through Homebridge.

## Baseline capture (before/after)

While thermostat is in **manual eco** and fan **idle**:

| Source | Record |
|--------|--------|
| HA States | `climate.nest_*`: `hvac_mode`, `hvac_action`, `preset_mode`, `fan_mode` |
| HA States | `switch.nest_*_eco`, `binary_sensor.nest_*_occupancy`, `_fan`, `_leaf` |
| MQTT | `nolongerevil/{serial}/ha/preset`, `mode`, `action`, `fan_mode`, `fan_running`, `occupancy`, `eco_switch` |
| Apple Home | Screenshot thermostat + nested fan (HA HomeKit Bridge only) |

## Hardware checklist

1. Confirm `climate.*` integration = **MQTT** (not patricktr custom)
2. Confirm add-on / Self-Hosted version is **0.0.17+**
3. Confirm `switch.nest_*_eco` exists in entity registry
4. Confirm **ha-homekit-nest-fan** integration is loaded
5. Record `hvac_mode`, `hvac_action`, `preset_mode`, temps before each test
6. **Eco switch On** → physical eco activates → switch stays On after refresh
7. **Eco switch Off** → exit eco → schedule resumes → switch Off
8. `climate.set_preset_mode` eco then home — both directions work
9. Add eco switch to HomeKit Bridge; toggle from Apple Home
10. Arrival automation: `switch.turn_off` on eco switch when person arrives
11. Automatic eco still activates after manual off (regression)
12. Fan tile vs `hvac_action` / `fan_running` — fan not "on" when blower idle
13. Manual eco + HVAC idle → Apple Home thermostat **OFF** (not heating/cooling)
14. Physically heating in eco → Apple Home shows heating (truthful)

## Acceptance criteria

| Scenario | Expected in HA | Expected in Apple Home |
|----------|----------------|------------------------|
| Manual eco, HVAC idle | preset=away/eco, action=idle, fan=auto | Thermostat OFF |
| Physically heating in eco | action=heating | Shows heating |
| Fan blower running | fan_running=true (fan_mode may stay auto) | HomeKit Active On via ha-homekit-nest-fan |
| Fan policy auto, blower idle | fan_mode=auto, fan_running=false | HomeKit Active Off, Target Auto |
| Fan timer on | fan_mode=on | HomeKit Target Manual |
| Manual eco enabled | occupancy=away (aligned) | No contradictory "home occupied on" |
| Single accessory goal | Only climate + eco switch in HK filter | One Nest thermostat tile + eco toggle |
| Eco switch On/Off | Matches physical eco | Toggle works from HomeKit |

## Sample automations

```yaml
# Exit eco before arrival (HomeKit-friendly)
- alias: NLE pre-warm on arrival
  triggers:
    - platform: state
      entity_id: person.you
      to: home
  actions:
    - action: switch.turn_off
      target:
        entity_id: switch.nest_XXXXXXXX_eco
    - action: climate.set_temperature
      target:
        entity_id: climate.nest_XXXXXXXX
      data:
        temperature: 72
```

```yaml
# Enable eco when away (optional)
- alias: NLE eco when away
  triggers:
    - platform: state
      entity_id: person.you
      to: not_home
      for: "00:15:00"
  actions:
    - action: switch.turn_on
      target:
        entity_id: switch.nest_XXXXXXXX_eco
```

## Rollback

1. Stop forked add-on
2. Re-enable official `codykociemba/NoLongerEvil-HomeAssistant` repository
3. Install/restore previous official add-on version
4. Restart Mosquitto
5. **Settings → Devices & Services → HomeKit Bridge** → reload
6. Remove stale `switch.nest_*_eco` entities if needed (MQTT discovery cleanup)
7. Optionally remove `ha_homekit_nest_fan` from `custom_components` and delete the integration

## After checklist passes

Open upstream PRs using `~/GitHub-Personal/nle-upstream-pr-drafts.md`.
