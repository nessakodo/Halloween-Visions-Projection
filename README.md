# Halloween Hand Detection Projection System 🎃👻

## Quick start
1) Install **Git LFS** for video file support: `git lfs install`
2) Create and activate a Python virtualenv (see DEMO_SETUP.md)  
3) Install requirements  
4) Use **VPT8 Mac version** (Intel build under Rosetta) - do **not** use VPT8 Silicon beta  
5) Remove VIDDLL package (see DEMO_SETUP.md)  
6) Configure sources and mix (1video, 2video, 8mix) and assign **8video** to your layer  
7) Run the YOLO→OSC bridge

### VPT8 setup (confirmed)
- Row 1 = idle (1video, On, Loop)
- Row 2 = scare (2video, On, Loop)
- Row 8 = mix (On, A=1video, B=2video, mode=mix)
- Layer = Source=**8video**, **fade=1.0**
- Bottom bar: blackout off
- **Row 8 thumbnail reflects the mix** on the working Mac version

### OSC integration
```bash
# Priming
/sources/1video/on 1
/sources/2video/on 1
/sources/8mix/on 1

# Crossfade
/sources/8mix/mix 0.0   # Idle
/sources/8mix/mix 1.0   # Scare
```
Float 0.0–1.0 crossfades; send ramps for smooth transitions.

### Run
```bash
python scripts/yolo_hand_scare_bridge.py --show   # with preview
python scripts/yolo_hand_scare_bridge.py          # headless
```

### Notes
- VPT8 Silicon beta's Mix module is broken; do not use it.
- Mapping and masks are applied at the **layer** level; the mix is just the layer's source.

### 🎥 Visual Setup Guide
<!-- ![Hand Detection Demo](docs/images/halloween-hand-detection-demo.gif) -->
**See [Visual Setup Guide](docs/images/) for VPT8 configuration screenshots**

## 🎬 How It Works

1. **Camera** captures real-time video feed
2. **YOLO model** classifies frames for hand presence (95% confidence threshold)
3. **OSC messages** control VPT8's row 8 mix fader
4. **Mix fader** blends between idle and scare videos
5. **Projection** shows seamless transition from calm to scary content

## ✨ Features

### 🖐️ Hand Detection
- **Fine-tuned YOLO model** (`best.pt`) for accurate hand classification
- **95% confidence threshold** prevents false positives
- **Real-time processing** at 30+ FPS
- **Any camera resolution** supported (auto-resized)

### 📷 Camera Selection
- **Automatic camera discovery** - scan for available cameras
- **Flexible source selection** - built-in, external, or video files
- **Easy switching** between laptop and USB cameras
- **Preview mode** to test camera positioning and detection

### 🎥 VPT8 Integration  
- **Mix fader control** via OSC (row 8 mixer)
- **Crash-resistant** (VIDDLL disabled, using AVFoundation)
- **Smooth transitions** between idle and scare states
- **2-second scare duration** with automatic return to idle

### 🔧 Production Ready
- **Comprehensive testing** with simulation and real detection
- **Robust error handling** and state management
- **Performance optimized** for live demonstrations
- **Emergency procedures** for troubleshooting

## 📁 Project Structure

```
├── scripts/                           # 🚀 Production scripts
│   ├── yolo_hand_scare_bridge.py      # 🎯 Main production script
│   ├── test_hand_detection_sim.py     # 🧪 Testing simulation
│   ├── test_osc_vpt.py                # 🔗 OSC communication test
│   ├── test_dependencies.py           # ✅ System verification
│   └── create_test_media.py           # 🎬 Media generation utility
├── media/                             # 🎥 Production media (stored with Git LFS)
│   ├── scare_awake.mp4                # 😱 Scare effect video
│   └── sleep_.mp4                     # 😴 Calm state video
├── models/                            # 🧠 YOLO models organized
│   ├── hand-detection/                # 🖐️ Fine-tuned hand models
│   │   ├── best_final.pt              # Alternative versions
│   │   ├── best_v2.pt                 # for testing
│   │   └── best_v3.pt                 # and comparison
│   └── general-detection/             # 🔍 General YOLO models
│       ├── yolo11n.pt                 # YOLO11 nano
│       └── yolov8n.pt                 # YOLO8 nano
├── best.pt                            # 🎯 Current production model
├── archive/                           # 📦 Legacy files (organized)
│   ├── scripts/                       # Old bridge versions
│   └── media/                         # Test media files
├── docs/DEMO_SETUP.md                 # 📖 Complete setup guide
└── CHANGELOG.md                       # 📝 Development history
```

## ⚙️ Configuration

### Main Script Options
```bash
python scripts/yolo_hand_scare_bridge.py [OPTIONS]

--model           YOLO model file (default: best.pt)
--source          Camera index (0=built-in, 1=external) or video file (default: 0)
--list-cameras    List available cameras and exit
--scare-conf      Confidence threshold for scare (default: 0.95)
--scare-duration  Scare duration in seconds (default: 2.0)
--show            Display detection window with confidence overlay
--debug           Enable verbose logging
```

### Camera Selection Examples
```bash
# Discover cameras
python scripts/yolo_hand_scare_bridge.py --list-cameras

# Use built-in laptop camera
python scripts/yolo_hand_scare_bridge.py --source 0 --show

# Use external USB camera
python scripts/yolo_hand_scare_bridge.py --source 1 --show

# Use video file for testing
python scripts/yolo_hand_scare_bridge.py --source /path/to/video.mp4 --show
```

### VPT8 Setup
- **Row 8 mixer**: Idle video → input 1, Scare video → input 2
- **OSC port**: 6666 (monitor incoming messages)
- **Engine**: AVFoundation (VIDDLL disabled)
- **Output**: Route row 8 to projection layer

## 🔧 Technical Details

### Hand Detection Model
- **Type**: Classification (hand vs not_hand)
- **Classes**: 2 classes with 100% validation accuracy
- **Architecture**: Fine-tuned YOLO for hand detection
- **Performance**: 30+ FPS real-time processing

### OSC Integration
- **Protocol**: OSC over UDP to VPT8
- **Primary path**: `/sources/8video/mixfader`
- **Redundant paths**: Multiple OSC paths for reliability
- **Values**: 0.0 = idle, 1.0 = scare

### State Machine
```
IDLE (mix=0.0) → Hand Detection (≥95% conf) → SCARE (mix=1.0)
     ↑                                              ↓
     ←←← Automatic Return (after 2 seconds) ←←←←←←←←
```

## 🛠️ Troubleshooting

### Camera Issues
- **"Cannot open camera"**: Run `--list-cameras` to see available options
- **Wrong camera**: Try `--source 1`, `--source 2`, etc.
- **Permission denied**: Check macOS Camera permissions in System Preferences
- **USB camera not working**: Unplug/replug, try different USB port

### Detection Issues  
- **No hand detection**: Lower `--scare-conf 0.90` or improve lighting
- **False triggers**: Increase `--scare-conf 0.98` or adjust camera angle
- **Poor accuracy**: Ensure good lighting, clean camera lens

### VPT8 Issues
- **VPT8 crashes**: Ensure VIDDLL is disabled (renamed to VIDDLL.disabled)
- **No OSC response**: Check VPT8 OSC monitor shows incoming messages
- **Mix fader not moving**: Verify row 8 mixer setup with test script

### Emergency Procedures
- **Stop script**: Press Ctrl+C
- **Reset to idle**: Run `python scripts/test_osc_vpt.py`
- **VPT8 recovery**: Restart VPT8 and reload project

## 📖 Documentation

- **[Complete Setup Guide](docs/DEMO_SETUP.md)** - Detailed configuration and troubleshooting
- **[Development History](CHANGELOG.md)** - Full development timeline and technical decisions

### 🎥 Viewing Media Files
Workshop demonstration videos are included and shared via **Git LFS**. For previewing video files and images in VS Code, install the [Video Preview extension](https://marketplace.visualstudio.com/items?itemName=BatchNepal.vscode-video-preview).

## 🎯 Demo Day Checklist

- [ ] ✅ VPT8 VIDDLL disabled (crash prevention)
- [ ] ✅ Hand detection model tested and calibrated
- [ ] ✅ OSC communication verified
- [ ] ✅ Row 8 mixer configured with videos
- [ ] ✅ Camera positioned and lighting optimized
- [ ] ✅ Emergency procedures reviewed

## 🏆 Status: Production Ready

The Halloween hand detection projection system is **fully operational** and **battle-tested**. Real-time hand detection successfully triggers scare effects through VPT8 projection mapping.

**Key Achievements:**
- ✅ **Crash-free VPT8 operation** 
- ✅ **Accurate hand detection** (95% confidence)
- ✅ **Smooth video transitions** 
- ✅ **Real-time performance** (30+ FPS)
- ✅ **Comprehensive documentation**

---

*Built with YOLO, VPT8, RunPod, and lots of Halloween spirit From the ML Visions Projects DenHac Haloween Crew!
Special Thanks to Mike CodeZero and Patrick Cromer for their efforts 🎃*