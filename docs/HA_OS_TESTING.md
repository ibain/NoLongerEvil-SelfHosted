# HA OS Testing — Forked NLE Add-on

## Fork repos

- https://github.com/ibain/NoLongerEvil-SelfHosted (`fix/eco-mode-control`)
- https://github.com/ibain/NoLongerEvil-HomeAssistant (`fix/eco-mode-control`)
- https://github.com/ibain/homebridge-nolongerevil-nest (`fix/eco-mode-control`)

## Install forked add-on

1. HA → **Settings → Add-ons → Add-on Store → Repositories**
2. Add: `https://github.com/ibain/NoLongerEvil-HomeAssistant`
3. Install **NoLongerEvil HomeAssistant** from your fork (stop official add-on first)
4. Set `api_origin` to `http://<HA-LAN-IP>:9543`
5. Enable **mqtt_minimal_discovery** in add-on options (or set `MQTT_MINIMAL_DISCOVERY=true`) to expose only `climate.*` + `switch.*_eco`
6. Restart Mosquitto + forked add-on
7. **Settings → Devices & Services → MQTT → Configure** → reload if entities stale

## HomeKit Bridge filter

Expose:

- `climate.nest_<serial>`
- `switch.nest_<serial>_eco`

Exclude:

- `binary_sensor.nest_*_occupancy`
- `binary_sensor.nest_*_fan`
- `binary_sensor.nest_*_leaf`
- diagnostic sensors (battery, rssi, etc.)

Long-term: use **one** bridge (HA HomeKit Bridge **or** homebridge-nolongerevil-nest), not both.

## Homebridge fork test

```bash
cd ~/GitHub-Personal/homebridge-nolongerevil-nest
git checkout fix/eco-mode-control
npm install && npm run build
# Point homebridge config at NLE self-hosted API (same host:9543)
```

## Baseline capture (before/after)

While thermostat is in **manual eco** and fan **idle**:

| Source | Record |
|--------|--------|
| HA States | `climate.nest_*`: `hvac_mode`, `hvac_action`, `preset_mode`, `fan_mode` |
| HA States | `switch.nest_*_eco`, `binary_sensor.nest_*_occupancy`, `_fan`, `_leaf` |
| MQTT | `nolongerevil/{serial}/ha/preset`, `mode`, `action`, `fan_mode`, `fan_running`, `occupancy`, `eco_switch` |
| Apple Home | Screenshot thermostat + fan tiles (both bridges if still dual) |

## Hardware checklist

1. Confirm `climate.*` integration = **MQTT** (not patricktr custom)
2. Confirm `switch.nest_*_eco` exists in entity registry
3. Record `hvac_mode`, `hvac_action`, `preset_mode`, temps before each test
4. **Eco switch On** → physical eco activates → switch stays On after refresh
5. **Eco switch Off** → exit eco → schedule resumes → switch Off
6. `climate.set_preset_mode` eco then home — both directions work
7. Add eco switch to HomeKit Bridge; toggle from Apple Home
8. Arrival automation: `switch.turn_off` on eco switch when person arrives
9. Automatic eco still activates after manual off (regression)
10. Fan tile vs `hvac_action` / `fan_running` — fan not "on" when blower idle
11. Manual eco + HVAC idle → Apple Home thermostat **OFF** (not heating/cooling)
12. Physically heating in eco → Apple Home shows heating (truthful)

## Acceptance criteria

| Scenario | Expected in HA | Expected in Apple Home |
|----------|----------------|------------------------|
| Manual eco, HVAC idle | preset=away/eco, action=idle, fan=auto | Thermostat OFF |
| Physically heating in eco | action=heating | Shows heating |
| Fan blower running | fan_mode=on OR fan_running=true | Fan reflects running |
| Fan commanded but blower off | fan_mode=auto, fan_running=false | Fan not "on" |
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

## After checklist passes

Open upstream PRs using `~/GitHub-Personal/nle-upstream-pr-drafts.md`.
