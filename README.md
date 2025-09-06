# Fine‑Tune + Projection Mapping (VPT POC)

Minimal proof‑of‑concept to trigger **VPT** (Video Projection Tools) playback from **YOLOv8** detections.

## Structure
```
media/               # put idle.mp4, scare.mp4 here
scripts/             # bridge scripts (YOLO -> OSC -> VPT)
vpt-presets/         # optional: exported VPT project/presets
docs/                # notes, screenshots
```

## Quick start (macOS, Apple Silicon ok)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/yolo_vpt_bridge.py --model /path/to/your_yolov8.pt --show
```
Then in **VPT**:
1. **Clip** tab → current source: `1video`
2. Add `media/idle.mp4` (Clip1) and `media/scare.mp4` (Clip2); enable *loop*.
3. **Active** panel → Layer 1 source=`1video`, opacity=1.0.
4. **OSC** panel → receive port **6666** (default). Output fullscreen on projector (Esc).

**OSC messages sent:**
- Idle → `/sources/1video/clipnr 1`, `/sources/1video/start`
- Scare → `/sources/1video/clipnr 2`, `/sources/1video/start`

## Notes
- Change source name in VPT? Update the OSC paths in the script.
- To use presets instead of clips: run `--mode presets` and make Preset 1/2 in VPT.
- For crossfades, see `yolo_vpt_bridge_crossfade.py`.
