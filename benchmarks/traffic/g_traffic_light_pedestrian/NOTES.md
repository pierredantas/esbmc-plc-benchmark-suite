# Provenance NOTES

- Source: https://github.com/beremiz/beremiz/tree/master/exemples/svghmi_traffic_light
- License: GPL-2.0-or-later (Beremiz project license; examples are part of the repository)
- Copied plc.xml verbatim (contains the LD/FB traffic_light_sequence POU).
- Uses TON timers for phase sequencing; inputs SWITCH_BUTTON, PEDESTRIAN_BUTTON; outputs RED/ORANGE/GREEN and pedestrian lights.
- Neither route currently verifies this program: the ladder route rejects its R_TRIG
  blocks (`UnsupportedConstruct(R_TRIG, tier=2)`), and the via-C route's `iec2c` step
  also rejects the compiled ST. Filed upstream as esbmc/esbmc#7483. See the recorded
  run at `results/records/g_traffic_light_pedestrian__plc.json`.
