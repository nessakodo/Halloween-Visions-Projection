# Fine‑Tune + Projection Mapping (VPT POC)

Minimal proof‑of‑concept to trigger **VPT** (Video Projection Tools) playback from **YOLOv8** detections.

## Structure
```
media/               # put idle.mp4, scare.mp4 here
scripts/             # bridge scripts (YOLO -> OSC -> VPT)
vpt-presets/         # optional: exported VPT project/presets
docs/                # notes, screenshots
```

## 🚀 Quick Start (Demo Ready!)

### 1. Environment Setup
```bash
cd "/Users/colinrooney/Dev/Active Projects/Halloween-Visions"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Test System
```bash
# Verify all dependencies work
python scripts/test_dependencies.py

# Test OSC communication to VPT
python scripts/test_osc_vpt.py
```

### 3. VPT Configuration
1. **Clip** tab → current source: `1video`
2. Add `media/idle.mp4` (Clip1) and `media/scare.mp4` (Clip2); enable **loop**
3. **Active** panel → Layer 1 source=`1video`, opacity=1.0
4. **OSC** panel → receive port **6666**, enable "Monitor in"
5. Output fullscreen on projector (**Esc**)

### 4. Run Demo
```bash
# Basic demo (any object detection)
python scripts/yolo_vpt_bridge.py --model yolov8n.pt --show

# Specific objects only (e.g., people and hands)
python scripts/yolo_vpt_bridge.py --model yolov8n.pt --show --class-names person hand

# Debug mode for troubleshooting
python scripts/yolo_vpt_bridge.py --model yolov8n.pt --show --debug
```

**Press ESC or Q to quit, Ctrl+C to stop**

## 📖 Complete Setup Guide
See [`docs/DEMO_SETUP.md`](docs/DEMO_SETUP.md) for detailed configuration and troubleshooting.

## ✨ What's Included

### Scripts
- **`yolo_vpt_bridge.py`** - Enhanced YOLO11-compatible bridge with logging
- **`yolo_vpt_bridge_crossfade.py`** - Smooth layer transitions  
- **`test_dependencies.py`** - Verify all packages and YOLO models
- **`test_osc_vpt.py`** - Test VPT communication
- **`create_test_media.py`** - Generate placeholder media files

### Media (Created Automatically)
- **`idle.mp4/png`** - Calm blue gradient for idle state
- **`scare.mp4/png`** - Intense red flashing for scare state

### Documentation
- **`DEMO_SETUP.md`** - Complete setup and troubleshooting guide
- **`.gitignore`** - Excludes large media and model files

## 🔧 Configuration

**OSC Messages:**
- Idle → `/sources/1video/clipnr 1`, `/sources/1video/start`
- Scare → `/sources/1video/clipnr 2`, `/sources/1video/start`

**Bridge Options:**
- `--model`: YOLO model (try `yolov8n.pt`, `yolo11n.pt`)
- `--source`: Camera (0,1,2) or video file
- `--conf`: Confidence threshold (0.1-1.0)
- `--class-names`: Filter specific objects
- `--cooldown`: Seconds between state changes
- `--debug`: Enable verbose logging

## 🎯 Demo Flow
1. VPT shows idle loop → 2. Run bridge → 3. Wave at camera → 4. Scare triggers → 5. Return to idle

## 🛠️ Troubleshooting
- **Camera issues**: Try `--source 1` or `--source 2`
- **No VPT switching**: Check OSC monitor, verify source name
- **Poor detection**: Lower `--conf 0.3`, enable `--debug`
- **Performance**: Use `yolov8n.pt` model, good lighting

**Status: ✅ Demo Ready - All core functionality implemented and tested**
