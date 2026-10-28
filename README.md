# MÖBIUS — Demo

A short, self-contained demo of MÖBIUS. Open `index.html` in a browser with WebGL 2 (headphones recommended).

## What happens

1. The intro cutscene plays, then you walk one loop of the Facility 7 service ring.
2. About halfway round, the lights stutter and die. When they come back, **the Harlequin** is right in your face. This happens once.
3. At the end of the loop the world flips and **the Thrum** forms in the corridor. OBVERSE tells you to crouch, but in the demo the Thrum lunges at you no matter what.
4. Instead of the death screen and retry, an **End of Demo** screen is chalked onto the black, with a *Play again* button.

Every run starts fresh: the demo doesn't save progress, and the save-slot menu is hidden.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The demo (built, single file). |
| `source/mobius.html` | The full game it is built from. |
| `tools/build_demo.py` | Patches the full game into the demo. |

## Rebuilding

The game is a single minified bundle, so the demo is made by exact-match patches. Each patch must match exactly once, or the build stops with an error.

```bash
python3 tools/build_demo.py
```

To tune the demo, change these values in `DEMO_JS` inside `tools/build_demo.py`:

- `at`: how far round the ring (in radians, about 5.4 for a full loop) you walk before the Harlequin strikes.
- `lunge`: how many seconds the Thrum waits after the "Crouch" warning before it jumps.
