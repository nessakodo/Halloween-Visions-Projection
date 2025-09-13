# Halloween Hand Detection Projection System 🎃👻

Real-time **hand detection** triggers **scare effects** in **VPT8** projection mapping. Wave your hand to activate spooky Halloween projections!

## 🚀 Quick Start

### 1. Setup Environment
```bash
cd "/Users/colinrooney/Dev/Active Projects/Halloween-Visions"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. VPT8 Version Requirements (CRITICAL!)
**Use VPT8 Silicon version, NOT the beta!**
- ✅ **macOS**: VPT8 Silicon version (mix module works)
- ⚠️ **Windows/PC**: Beta has broken mix module - needs update
- ❌ **Avoid**: VPT8 beta (2+ years old, non-functional mix module)

### 3. Configure VPT8 (Crash Prevention Required!)
```bash
# IMPORTANT: Disable VIDDLL to prevent crashes
open /Applications/VPT8.app/Contents/Resources/C74/packages/
mv VIDDLL VIDDLL.disabled
```

### 4. Test System
```bash
# Verify OSC communication
python scripts/test_osc_vpt.py

# Test hand detection simulation
python scripts/test_hand_detection_sim.py
```

### 5. Run Production System
```bash
# Real-time hand detection with preview
python scripts/yolo_hand_scare_bridge.py --show

# Production mode (no preview)
python scripts/yolo_hand_scare_bridge.py
```

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
├── media/                             # 🎥 Production media
│   ├── idle.mp4                       # 😴 Calm state video
│   └── scare.mp4                      # 😱 Scare effect video
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
--source          Camera index or video file (default: 0)
--scare-conf      Confidence threshold for scare (default: 0.95)
--scare-duration  Scare duration in seconds (default: 2.0)
--show            Display detection window
--debug           Enable verbose logging
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

### Common Solutions
- **Camera issues**: Try `--source 1` or check permissions
- **VPT8 crashes**: Ensure VIDDLL is disabled 
- **No detection**: Lower `--scare-conf 0.90` or improve lighting
- **False triggers**: Increase `--scare-conf 0.98` or adjust camera angle

### Emergency Procedures
- **Stop script**: Press Ctrl+C
- **Reset to idle**: Run `python scripts/test_osc_vpt.py`
- **VPT8 recovery**: Restart VPT8 and reload project

## 📖 Documentation

- **[Complete Setup Guide](docs/DEMO_SETUP.md)** - Detailed configuration and troubleshooting
- **[Development History](CHANGELOG.md)** - Full development timeline and technical decisions

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

*Built with YOLO11, VPT8, and lots of Halloween spirit! 🎃*