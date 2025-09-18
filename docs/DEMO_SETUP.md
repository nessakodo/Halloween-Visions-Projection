# Halloween Hand Detection Projection - Setup Guide

## 🎃 Quick Setup (5-10 minutes)

### 1. Environment Setup
```bash
# Navigate to project
cd "/Users/colinrooney/Dev/Active Projects/Halloween-Visions"

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. VPT8 Version Requirements (CRITICAL!)

**IMPORTANT: Use VPT8 Silicon version, NOT the beta!**

- ✅ **macOS**: Use **VPT8 Silicon version** - mix module works correctly
- ⚠️ **Windows/PC**: **Beta version has broken mix module** - needs PC-compatible VPT8 version
- ❌ **Avoid**: VPT8 beta (2+ years old) - mix module in source section is non-functional

### 3. VPT8 Crash Prevention (IMPORTANT!)
**Must do this first to prevent crashes:**

1. **Quit VPT8 completely**
2. **Disable VIDDLL engine:**
   ```bash
   # Navigate to VPT8 packages
   open /Applications/VPT8.app/Contents/Resources/C74/packages/
   
   # Rename VIDDLL folder to disable it
   mv VIDDLL VIDDLL.disabled
   ```
3. **Update VPT8 preferences** (in project folder):
   ```
   preview 0
   previewframerate 10
   framerate 15
   ```

### 4. VPT8 Configuration

#### In VPT8:
1. **Row 8 Mixer Setup**:
   - Route idle video to **one input** of row 8 mixer
   - Route scare video to **another input** of row 8 mixer
   - Both videos should be playing and looping

2. **Layer Configuration**:
   - Route **row 8 output** to your projection layer
   - Set layer opacity to 1.0

3. **OSC Setup**:
   - Go to **OSC** panel
   - Verify receive port = `6666`
   - Enable "Monitor in" to see incoming messages

4. **Output**:
   - Press **Esc** to fullscreen Output window on projector

### 5. Camera Setup and Selection

#### Discover Available Cameras:
```bash
# Scan for all working cameras
python scripts/yolo_hand_scare_bridge.py --list-cameras
```

#### Test Camera Selection:
```bash
# Test built-in laptop camera (usually camera 0)
python scripts/yolo_hand_scare_bridge.py --source 0 --show

# Test external/USB camera (usually camera 1)
python scripts/yolo_hand_scare_bridge.py --source 1 --show

# Test additional cameras if available
python scripts/yolo_hand_scare_bridge.py --source 2 --show
```

**Camera Selection Tips:**
- **Built-in camera**: Usually good for close-range detection
- **External USB camera**: Often better for projection mapping setups
- **Positioning**: Place camera where it can clearly see the target area
- **Lighting**: Ensure good lighting for best detection accuracy

### 6. Test System
```bash
# Test OSC mix fader control (should see fader moving in VPT8)
python scripts/test_osc_vpt.py

# Optional: Test hand detection simulation
python scripts/test_hand_detection_sim.py
```

### 7. Run Hand Detection System

#### Production System:
```bash
# Production mode with built-in camera (no preview)
python scripts/yolo_hand_scare_bridge.py

# Production mode with external camera
python scripts/yolo_hand_scare_bridge.py --source 1

# Preview mode for setup (shows detection window)
python scripts/yolo_hand_scare_bridge.py --source 1 --show

# Debug mode for troubleshooting
python scripts/yolo_hand_scare_bridge.py --source 1 --show --debug
```

## 🎬 Demo Flow

1. **Start VPT8** - row 8 should show blended idle/scare videos
2. **Run hand detection script** - connects to VPT8 via OSC
3. **Show hand to camera** - 95% confidence triggers scare effect
4. **Remove hand** - returns to idle after 2 seconds
5. **Press Q or ESC** - quit the demo

## ⚙️ Configuration Options

### Hand Detection Script Parameters
- `--model`: YOLO model (default: `best.pt` - fine-tuned hand classifier)
- `--source`: Camera index (0=built-in, 1=external, etc.) or video file path
- `--list-cameras`: List all available cameras and exit (for discovery)
- `--scare-conf`: Confidence threshold for scare trigger (default: 0.95)
- `--scare-duration`: Seconds in scare mode (default: 2.0)
- `--show`: Display detection window with confidence overlay
- `--debug`: Enable verbose logging

### Advanced Configuration
```bash
# Lower confidence threshold (more sensitive)
python scripts/yolo_hand_scare_bridge.py --show --scare-conf 0.90

# Longer scare duration
python scripts/yolo_hand_scare_bridge.py --show --scare-duration 3.0

# Different camera
python scripts/yolo_hand_scare_bridge.py --show --source 1
```

## 🔧 Technical Details

### Hand Detection Model
- **Type**: Classification model (not detection)
- **Classes**: `hand` vs `not_hand`
- **Input**: Any camera resolution (auto-resized to 224x224)
- **Performance**: 30+ FPS real-time
- **Confidence**: 95% threshold prevents false positives

### VPT8 Integration
- **Method**: Row 8 mix fader control via OSC
- **OSC Paths**: `/sources/8video/mixfader`, `/sources/8/mix`, etc.
- **Mix Values**: 0.0 = idle video, 1.0 = scare video
- **Engine**: AVFoundation (VIDDLL disabled for stability)

### State Machine
- **Idle State**: Mix fader at 0.0, showing idle video
- **Trigger**: Hand detected with ≥95% confidence
- **Scare State**: Mix fader at 1.0, showing scare video
- **Return**: Automatic return to idle after 2 seconds

## 🛠️ Troubleshooting

### Common Issues

1. **VPT8 Crashes**:
   - ✅ **FIXED**: VIDDLL disabled, using AVFoundation
   - Ensure VIDDLL folder is renamed to `VIDDLL.disabled`

2. **Camera Issues**:
   - **"Cannot open camera"**: Run `--list-cameras` first to see available options
   - **Wrong camera**: Try `--source 1`, `--source 2` for external cameras
   - **Permission denied**: Check macOS Camera permissions in System Preferences
   - **USB camera not detected**: Unplug/replug USB cable, try different port
   - **Camera shows black screen**: Check if another app is using the camera

3. **No OSC response in VPT8**:
   - Check OSC monitor shows incoming messages
   - Verify row 8 mix fader moves when running `test_osc_vpt.py`
   - Ensure videos are properly routed to row 8 inputs

4. **No hand detection**:
   - Lower confidence: `--scare-conf 0.85`
   - Enable debug mode: `--debug`
   - Check camera positioning and lighting

5. **False triggers**:
   - Increase confidence: `--scare-conf 0.98`
   - Check for body positions triggering false positives
   - Improve camera angle to focus on hands only

### Performance Tips

- **Lighting**: Good lighting improves detection accuracy significantly
- **Camera Position**: Position camera to clearly see target area
- **Background**: Minimize background clutter
- **Model**: `best.pt` is optimized for hand detection
- **Hardware**: Dedicated GPU improves performance

### OSC Debugging
```bash
# Test OSC communication separately
python scripts/test_osc_vpt.py

# Monitor VPT8 OSC messages in real-time
# Enable "Monitor in" in VPT8 OSC panel
```

## 📋 Demo Day Checklist

### Pre-Setup
- [ ] VPT8 VIDDLL disabled (prevents crashes)
- [ ] VPT8 preferences updated (preview=0, framerate=15)
- [ ] VPT8 Silicon version installed (not beta)

### Camera Setup
- [ ] Camera discovery completed (`--list-cameras`)
- [ ] Optimal camera selected (built-in vs external)
- [ ] Camera positioning optimized for target area
- [ ] Camera permissions granted in macOS
- [ ] Lighting optimized for hand detection

### VPT8 Configuration
- [ ] Row 8 mixer configured with idle/scare videos
- [ ] OSC communication tested and working (`test_osc_vpt.py`)
- [ ] Mix fader responds to OSC commands
- [ ] Projector/output configured and tested

### Hand Detection System
- [ ] Hand detection model (`best.pt`) loaded and tested
- [ ] Confidence threshold calibrated (default 95%)
- [ ] Detection tested with selected camera (`--show`)
- [ ] Production mode tested without preview

### Emergency Procedures
- [ ] Backup procedures known (Ctrl+C to stop)
- [ ] Manual reset procedure tested (`test_osc_vpt.py`)
- [ ] Alternative camera indices identified

## 🚨 Emergency Procedures

**If hand detection gets stuck:**
- Press **Ctrl+C** to stop the script
- VPT8 will remain in last state (idle or scare)
- Run `python scripts/test_osc_vpt.py` to manually reset to idle

**If VPT8 becomes unresponsive:**
- Close VPT8 completely
- Restart VPT8
- Reload your project configuration

---

**Status: ✅ Production Ready - Hand detection system fully operational with VPT8 integration**