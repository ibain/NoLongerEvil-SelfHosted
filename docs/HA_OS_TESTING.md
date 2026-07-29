# HA OS Testing — Forked NLE Add-on

## Fork repos

- https://github.com/ibain/NoLongerEvil-SelfHosted (`fix/eco-mode-control`)
- https://github.com/ibain/NoLongerEvil-HomeAssistant (`fix/eco-mode-control`)

## Install forked add-on

1. HA → **Settings → Add-ons → Add-on Store → Repositories**
2. Add: `https://github.com/ibain/NoLongerEvil-HomeAssistant`
3. Install **NoLongerEvil HomeAssistant** from your fork (stop official add-on first)
4. Set `api_origin` to `http://<HA-LAN-IP>:9543`
5. Optional: set env `MQTT_MINIMAL_DISCOVERY=true` to expose only `climate.*` + `switch.*_eco`
6. Restart Mosquitto + forked add-on

## HomeKit Bridge filter

Expose:

- `climate.nest_<serial>`
- `switch.nest_<serial>_eco`

Exclude occupancy/fan/leaf binary sensors unless debugging.

## Hardware checklist

See `~/GitHub-Personal/nle-deployment-notes.md` and plan acceptance criteria.

## Rollback

Re-enable official add-on repository, restore previous version, reload HomeKit Bridge.
