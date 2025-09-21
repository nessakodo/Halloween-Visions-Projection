# Halloween Hand Detection Projection System 🎃👻

## Quick start
1) Install **Git LFS** for video file support: `git lfs install`
2) Create and activate a Python virtualenv (see DEMO_SETUP.md)  
3) Install requirements: `pip install -r requirements.txt`
4) Use **HeavyM** projection mapping software (Demo version works!)
5) Run the YOLO→HeavyM bridge

### HeavyM Setup (MIDI Integration)
- **MIDI Mode**: Works with HeavyM Demo (free version)
- Create sequences: **sleepseq** (idle/ambient) and **scareseq** (scare content)
- Enable MIDI input in **Preferences > Controls > MIDI**
- Use **MIDI Learning** to map:
  - **Note 60 (C4)** → sleepseq Play button
  - **Note 61 (C#4)** → scareseq Play button

### Run
```bash
python scripts/yolo_hand_scare_bridge.py --show   # MIDI mode (default)
python scripts/yolo_hand_scare_bridge.py --use-osc --show   # OSC mode (Pro only)
```

### 🎹 MIDI Integration (Demo Compatible)
```bash
# Test MIDI connection
python send_midi_test.py --sequence both

# Setup macOS MIDI (if needed)
python setup_macos_midi.py
```

**Problem Solved**: HeavyM Demo's OSC API limitation → MIDI mapping solution
**macOS Issue**: Virtual MIDI ports → IAC Driver integration

### 🎥 Visual Setup Guide
**See [HeavyM MIDI Setup Guide](HEAVYM_MIDI_SETUP.md) for complete configuration**

## 🎬 How It Works

1. **Camera** captures real-time video feed
2. **YOLO model** classifies frames for hand presence (99% confidence threshold)
3. **MIDI messages** trigger HeavyM sequence changes
4. **HeavyM sequences** switch between idle and scare content
5. **Projection** shows seamless transition from calm to scary content

## ✨ Features

### 🖐️ Hand Detection
- **Fine-tuned YOLO model** (`best.pt`) for accurate hand classification
- **99% confidence threshold** prevents false positives
- **Real-time processing** at 30+ FPS
- **Any camera resolution** supported (auto-resized)

### 📷 Camera Selection
- **Automatic camera discovery** - scan for available cameras
- **Flexible source selection** - built-in, external, or video files
- **Easy switching** between laptop and USB cameras
- **Preview mode** to test camera positioning and detection

### 🎥 HeavyM Integration  
- **MIDI sequence control** compatible with Demo version
- **Dual mode support** - MIDI (default) or OSC (Pro)
- **Virtual MIDI port** creation for seamless integration
- **2-second scare duration** with automatic return to idle

### 🔧 Production Ready
- **Comprehensive testing** with simulation and real detection
- **Robust error handling** and state management
- **Performance optimized** for live demonstrations
- **Emergency procedures** for troubleshooting

## 📁 Project Structure

```
├── scripts/                           # 🚀 Production scripts
│   └── yolo_hand_scare_bridge.py      # 🎯 Main production script (MIDI + OSC)
├── send_midi_test.py                  # 🎹 MIDI testing utility
├── setup_macos_midi.py                # 🍎 macOS MIDI configuration helper
├── test_midi_port.py                  # 🔍 MIDI port diagnostics
├── osc_listener.py                    # 📡 OSC monitoring (for Pro users)
├── HEAVYM_MIDI_SETUP.md               # 📖 HeavyM setup guide
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
└── docs/DEMO_SETUP.md                 # 📖 Complete setup guide
```

## ⚙️ Configuration

### Main Script Options
```bash
python scripts/yolo_hand_scare_bridge.py [OPTIONS]

--model           YOLO model file (default: best.pt)
--source          Camera index (0=built-in, 1=external) or video file (default: 0)
--list-cameras    List available cameras and exit
--scare-conf      Confidence threshold for scare (default: 0.90)
--scare-duration  Scare duration in seconds (default: 2.0)
--use-midi        Use MIDI output (default: True for Demo compatibility)
--use-osc         Use OSC output instead of MIDI (for Pro version)
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

### HeavyM Setup
- **MIDI Input**: Enable in Preferences > Controls > MIDI
- **Sequences**: Create sleepseq (idle) and scareseq (scare)
- **MIDI Learning**: Map Note 60 → sleepseq, Note 61 → scareseq
- **Virtual Port**: "YOLO-HeavyM Bridge" (auto-created)

## 🔧 Technical Details

### Hand Detection Model
- **Type**: Classification (hand vs not_hand)
- **Classes**: 2 classes with 100% validation accuracy
- **Architecture**: Fine-tuned YOLO for hand detection
- **Performance**: 30+ FPS real-time processing

### HeavyM Integration
- **MIDI Mode**: Note 60 (C4) = sleepseq, Note 61 (C#4) = scareseq
- **OSC Mode**: `/sequences/sleepseq/play 1.0` and `/sequences/scareseq/play 1.0`
- **Dual Support**: Automatic fallback between MIDI and OSC
- **Port Creation**: Virtual MIDI port for seamless connection

### State Machine
```
IDLE (Note 60) → Hand Detection (≥99% conf) → SCARE (Note 61)
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
- **No hand detection**: Lower `--scare-conf 0.85` or improve lighting
- **False triggers**: Increase `--scare-conf 0.95` or adjust camera angle
- **Poor accuracy**: Ensure good lighting, clean camera lens

### MIDI Issues
- **Port not visible**: Enable IAC Driver in Audio MIDI Setup (macOS)
- **MIDI not working**: Run `python setup_macos_midi.py` for configuration
- **HeavyM not responding**: Check MIDI Learning mapping in Preferences

### HeavyM Issues
- **Sequences not switching**: Verify MIDI mapping and sequence names
- **Only scare works**: Ensure sleepseq Play button is mapped to Note 60
- **No MIDI input**: Check "Device is online" in IAC Driver settings

### Emergency Procedures
- **Stop script**: Press Ctrl+C
- **Test MIDI**: Run `python send_midi_test.py --sequence both`
- **Reset sequences**: Manually trigger sequences in HeavyM

## 📖 Documentation

- **[HeavyM MIDI Setup Guide](HEAVYM_MIDI_SETUP.md)** - Complete HeavyM configuration
- **[Complete Setup Guide](docs/DEMO_SETUP.md)** - Detailed configuration and troubleshooting
- **[Development History](CHANGELOG.md)** - Full development timeline and technical decisions

### Problems Solved
1. **HeavyM Demo OSC Limitation** → MIDI mapping solution (Note 60/61)
2. **macOS Virtual MIDI Issues** → IAC Driver integration  
3. **Port Conflicts** → Unified MIDI/OSC dual-mode approach

## 🎯 Demo Day Checklist

- [ ] ✅ HeavyM MIDI input enabled
- [ ] ✅ IAC Driver configured (macOS) 
- [ ] ✅ Hand detection model tested and calibrated
- [ ] ✅ MIDI communication verified
- [ ] ✅ Sequences created and mapped
- [ ] ✅ Camera positioned and lighting optimized
- [ ] ✅ Emergency procedures reviewed

## 🏆 Status: Production Ready

The Halloween hand detection projection system is **fully operational** and **HeavyM compatible**. Real-time hand detection successfully triggers scare effects through HeavyM projection mapping using MIDI integration.

**Key Achievements:**
- ✅ **HeavyM Demo compatibility** (free version works!)
- ✅ **MIDI bridge implementation** (virtual port creation)
- ✅ **Accurate hand detection** (99% confidence)
- ✅ **Smooth sequence transitions** 
- ✅ **Real-time performance** (30+ FPS)
- ✅ **Comprehensive documentation**

---

*Built with YOLO, HeavyM, and lots of Halloween spirit! From the ML Visions Projects DenHac Halloween Crew!
Special Thanks to Mike CodeZero and Patrick Cromer for their efforts 🎃*