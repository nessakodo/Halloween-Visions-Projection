# DEMO_SETUP.md

## 🎃 Quick Setup (5–10 minutes)

### 0) Prerequisites
**Git LFS** (required for video files):
```bash
git lfs install
```

**HeavyM Download:**
Download HeavyM from the official website. The **Demo version works** with our MIDI integration!

### 1) Environment setup (virtualenv)
```bash
# Navigate to your project directory
cd /path/to/Halloween-Visions-HeavyM

# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
To leave the venv later: `deactivate`

### 2) HeavyM Setup (MIDI Integration)
- ✅ Use **HeavyM Demo** (free version with watermark)
- ✅ **MIDI mapping** works in Demo version
- ✅ No Pro license required for basic sequence control

### 3) macOS MIDI Configuration
**Enable IAC Driver** (required for virtual MIDI):
1. Open **Audio MIDI Setup** (Applications > Utilities)
2. Window > **Show MIDI Studio**
3. Double-click **IAC Driver**
4. ✅ Check **"Device is online"**
5. Add port named **"YOLO-HeavyM"** (optional)
6. Click **Apply**

**Test MIDI setup:**
```bash
python setup_macos_midi.py
```

### 4) HeavyM Project Setup
**Create Sequences:**
1. Create new sequence: **sleepseq** (idle/ambient content)
2. Create new sequence: **scareseq** (scare/activation content)
3. Ensure sequences are **not marked as Draft**

**Configure MIDI Input:**
1. **Preferences** > **Controls** > **MIDI**
2. Select **"IAC Driver Bus 1"** or **"YOLO-HeavyM"** as input
3. Enable **MIDI Learning** mode
4. Click **sleepseq Play** button → Run: `python send_midi_test.py --sequence sleep`
5. Click **scareseq Play** button → Run: `python send_midi_test.py --sequence scare`
6. Disable **MIDI Learning** mode

### 5) Test the Integration
**Test MIDI Connection:**
```bash
# Test both sequences
python send_midi_test.py --sequence both

# Test individual sequences
python send_midi_test.py --sequence sleep
python send_midi_test.py --sequence scare
```

**Test Hand Detection:**
```bash
# Run with camera preview
python scripts/yolo_hand_scare_bridge.py --show

# List available cameras
python scripts/yolo_hand_scare_bridge.py --list-cameras
```

### 6) Production Run
```bash
# MIDI mode (default, works with Demo)
python scripts/yolo_hand_scare_bridge.py --show

# OSC mode (for Pro users)
python scripts/yolo_hand_scare_bridge.py --use-osc --show
```

## 🔧 Troubleshooting

### MIDI Issues
**"MIDI port not visible in HeavyM":**
1. Restart HeavyM after enabling IAC Driver
2. Check "Device is online" in Audio MIDI Setup
3. Run `python test_midi_port.py` to verify port creation

**"MIDI notes not triggering sequences":**
1. Verify MIDI Learning mapped correct notes (60 & 61)
2. Check sequences are not marked as Draft
3. Test with `python send_midi_test.py --sequence both`

### Camera Issues
**"Cannot open camera":**
```bash
# Check available cameras
python scripts/yolo_hand_scare_bridge.py --list-cameras

# Try different camera indices
python scripts/yolo_hand_scare_bridge.py --source 1 --show
```

**"Permission denied":**
- Check macOS Camera permissions in System Preferences > Security & Privacy

### Hand Detection Issues
**"No hand detection":**
- Lower confidence threshold: `--scare-conf 0.85`
- Improve lighting conditions
- Clean camera lens

**"Too many false triggers":**
- Raise confidence threshold: `--scare-conf 0.95`
- Adjust camera angle to avoid background movement

### HeavyM Issues
**"Sequences not switching":**
1. Verify sequence names exactly: **sleepseq** and **scareseq**
2. Check MIDI mapping in Preferences > Controls > MIDI
3. Ensure sequences are not in Draft mode

**"Only scare sequence works":**
- Check sleepseq Play button is mapped to Note 60 (C4)
- Verify idle state is being triggered (check bridge logs)

## 🎯 Demo Day Checklist

**Before the Event:**
- [ ] ✅ HeavyM installed and MIDI configured
- [ ] ✅ IAC Driver enabled and working
- [ ] ✅ Python environment activated
- [ ] ✅ All dependencies installed
- [ ] ✅ YOLO model (best.pt) in place
- [ ] ✅ Camera permissions granted
- [ ] ✅ Sequences created and mapped
- [ ] ✅ MIDI communication tested

**During Setup:**
- [ ] ✅ Camera positioned and focused
- [ ] ✅ Lighting optimized for detection
- [ ] ✅ Hand detection tested and calibrated
- [ ] ✅ Sequence transitions verified
- [ ] ✅ Emergency stop procedures reviewed

**Emergency Commands:**
```bash
# Stop bridge
Ctrl+C

# Test MIDI manually
python send_midi_test.py --sequence both

# Reset to idle
python send_midi_test.py --sequence sleep

# Debug mode
python scripts/yolo_hand_scare_bridge.py --debug --show
```

## 🏆 Expected Performance

**Hand Detection:**
- **Accuracy**: 99%+ confidence threshold
- **Speed**: 30+ FPS real-time processing
- **Latency**: <100ms from detection to sequence trigger

**MIDI Integration:**
- **Reliability**: Virtual MIDI port auto-creation
- **Compatibility**: Works with HeavyM Demo (free)
- **Responsiveness**: Immediate sequence switching

**System Requirements:**
- **macOS**: 10.14+ (for IAC Driver support)
- **Camera**: Built-in or USB camera
- **Memory**: 4GB+ RAM for YOLO processing
- **Storage**: 2GB+ for models and media

---

*This setup guide ensures reliable operation for Halloween demonstrations with HeavyM projection mapping! 🎃*