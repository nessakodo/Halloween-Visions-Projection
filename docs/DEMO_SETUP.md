# Halloween Projection Mapping - Demo Setup Guide

## Quick Setup (5-10 minutes)

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

### 2. Test Dependencies
```bash
# Run comprehensive dependency test
python scripts/test_dependencies.py
```

### 3. VPT Configuration

#### In VPT:
1. **Source Setup**:
   - Go to **Clip** tab
   - Set current source to: `1video`

2. **Add Media**:
   - In Playlist, click the file button
   - Add `media/idle.mp4` (this becomes Clip1)
   - Add `media/scare.mp4` (this becomes Clip2)
   - Enable **Loop** (slider 0→1) for both clips

3. **Layer Configuration**:
   - Go to **Active** panel (right side)
   - On Layer 1: Set source dropdown to `1video`
   - Set opacity to 1.0

4. **OSC Setup**:
   - Go to **OSC** panel
   - Verify receive port = `6666`
   - Optional: Enable "Monitor in" to see incoming messages

5. **Output**:
   - Press **Esc** to fullscreen Output window on projector
   - Or configure Output window to your projection setup

### 4. Test OSC Communication
```bash
# Test OSC messages to VPT (run while VPT is open)
python scripts/test_osc_vpt.py
```
Watch VPT - you should see clips switching automatically.

### 5. Run the Bridge

#### Basic Test (without camera):
```bash
# Test with built-in YOLO model
python scripts/yolo_vpt_bridge.py --model yolov8n.pt --source media/idle.mp4 --show
```

#### Live Camera Demo:
```bash
# Live camera with any object detection
python scripts/yolo_vpt_bridge.py --model yolov8n.pt --show

# Live camera with specific classes (e.g., only hands)
python scripts/yolo_vpt_bridge.py --model yolov8n.pt --show --class-names person hand

# Debug mode for troubleshooting
python scripts/yolo_vpt_bridge.py --model yolov8n.pt --show --debug
```

## Demo Flow

1. **Start VPT** - should show idle.mp4 looping
2. **Run bridge script** - connects to VPT via OSC
3. **Wave at camera** - detection triggers switch to scare.mp4
4. **Stop waving** - returns to idle.mp4 after cooldown
5. **Press Q or ESC** - quit the demo

## Configuration Options

### Bridge Script Parameters
- `--model`: YOLO model path (try `yolov8n.pt`, `yolov8s.pt`, or your trained model)
- `--source`: Camera index (0, 1, 2...) or video file path
- `--conf`: Confidence threshold (0.1-1.0, default: 0.6)
- `--cooldown`: Seconds between state changes (default: 1.5)
- `--class-names`: Only trigger on specific classes (e.g., `person hand`)
- `--show`: Display detection window
- `--debug`: Enable verbose logging

### VPT Configuration
- **Source name**: Change from `1video` to match your OSC paths in script
- **Clips vs Presets**: Use `--mode presets` for preset switching instead of clips
- **Multiple layers**: Use crossfade script for smooth transitions

## Troubleshooting

### Common Issues

1. **"Cannot open camera"**:
   - Try different camera indices: `--source 1`, `--source 2`
   - Check camera permissions in macOS System Preferences

2. **VPT not switching**:
   - Verify OSC monitor shows incoming messages
   - Check VPT source name matches script (default: `1video`)
   - Test manually with `python scripts/test_osc_vpt.py`

3. **No detections**:
   - Lower confidence: `--conf 0.3`
   - Enable debug mode: `--debug`
   - Test with any detection: remove `--class-names`

4. **Poor performance**:
   - Use smaller model: `yolov8n.pt` instead of `yolov8s.pt`
   - Reduce image size: modify `imgsz=640` to `imgsz=320` in script

### Advanced Configuration

#### Multiple Projectors
Modify script to send different OSC paths:
```python
# Projector A (mask)
osc.send_message("/sources/1video/clipnr", clip_num)
# Projector B (background)  
osc.send_message("/sources/2video/clipnr", clip_num)
```

#### Custom Gestures
Train YOLO on your specific gestures:
1. Collect gesture images
2. Label with YOLO format
3. Fine-tune model
4. Use with `--class-names your_gesture`

#### Crossfade Transitions
```bash
# Use smooth layer crossfade instead of hard cuts
python scripts/yolo_vpt_bridge_crossfade.py --model yolov8n.pt --rise 0.5
```

## Performance Tips

- **YOLO11 models**: Use `yolo11n.pt` for best speed/accuracy balance
- **Hardware**: Dedicated GPU improves performance significantly
- **Lighting**: Good lighting improves detection accuracy
- **Camera position**: Position camera to clearly see target area
- **Background**: Minimize background clutter for better detection

## Demo Day Checklist

- [ ] VPT project saved and tested
- [ ] Media files in correct location
- [ ] OSC communication verified
- [ ] Camera positioned and tested
- [ ] Projector/output configured
- [ ] Backup YOLO models ready
- [ ] Scripts tested end-to-end
- [ ] Emergency stop procedure known (Ctrl+C)