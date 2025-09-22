# VLC Direct Projection Setup Guide 🎬

## Overview
This setup uses **python-vlc** to directly project videos based on YOLO hand detection, eliminating the need for external mapping software like HeavyM or VPT8.

## Quick Start

### 1. Install Prerequisites
```bash
# Install VLC Media Player (download from videolan.org)
# - macOS: Download VLC-*.dmg and install
# - Windows: Download VLC-*-win64.exe and install

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Setup Video Files
```bash
# Create videos directory and add your content
python test_vlc_playback.py --create-test-videos

# Add your video files:
# videos/sleeping_face.mp4 - Idle/calm content for when no hands detected
# videos/angry_face.mp4 - Scare/alert content for when hands detected
```

### 3. Setup Projector Display
```bash
# List available displays
python scripts/yolo_vlc_projection.py --list-displays

# Configure OS display settings:
# - Set projector as extended display (not mirrored)
# - Note which display index corresponds to projector (usually 1)
```

### 4. Test Setup
```bash
# Test camera detection
python scripts/yolo_vlc_projection.py --list-cameras

# Test VLC playback (windowed)
python test_vlc_playback.py --video videos/sleeping_face.mp4 --duration 5

# Test fullscreen on projector (replace 1 with your projector display index)
python test_vlc_playback.py --video videos/sleeping_face.mp4 --fullscreen --display 1 --duration 5
```

### 5. Run Full System
```bash
# Basic run with camera preview
python scripts/yolo_vlc_projection.py --show

# Run with projector fullscreen (replace 1 with your display index)
python scripts/yolo_vlc_projection.py --fullscreen-display 1

# Run with custom video files
python scripts/yolo_vlc_projection.py --video-sleep my_idle.mp4 --video-scare my_scare.mp4 --fullscreen-display 1
```

## System Architecture

### State Machine
```
IDLE STATE (sleeping_face.mp4)
    ↓ Hand detected (≥99% confidence)
SCARE STATE (angry_face.mp4)
    ↓ After 2 seconds
IDLE STATE (sleeping_face.mp4)
```

### Video Switching Logic
- **Debounce**: 0.5s minimum between state changes (prevents flickering)
- **Loop**: Videos loop indefinitely until state change
- **Fullscreen**: Automatic fullscreen on specified display
- **Seamless**: Instant switching between videos

## Configuration Options

### Command Line Arguments
```bash
python scripts/yolo_vlc_projection.py [OPTIONS]

--model             YOLO model file (default: best.pt)
--source            Camera index or video file (default: 0)
--scare-conf        Hand confidence threshold (default: 0.99)
--scare-duration    Scare duration in seconds (default: 2.0)
--video-sleep       Path to idle video (default: videos/sleeping_face.mp4)
--video-scare       Path to scare video (default: videos/angry_face.mp4)
--fullscreen-display Display index for projection (default: None = windowed)
--show              Show camera preview window
--debug             Enable debug logging
```

### Display Setup Examples
```bash
# Find your projector display
python scripts/yolo_vlc_projection.py --list-displays

# Typical setups:
# - Laptop only: Don't use --fullscreen-display (windowed mode)
# - Laptop + projector: --fullscreen-display 1
# - Desktop + dual monitors: --fullscreen-display 1 or 2
```

## Video File Requirements

### Supported Formats
- **Recommended**: MP4 (H.264 codec)
- **Also supported**: AVI, MOV, MKV, WMV (any VLC-compatible format)

### Video Guidelines
- **Resolution**: Any resolution (VLC will scale to fit display)
- **Duration**: Any length (videos loop automatically)
- **Content**:
  - `sleeping_face.mp4`: Calm, idle content (faces, ambient scenes)
  - `angry_face.mp4`: Scare, alert content (scary faces, jump scares)

### Test Video Creation
If you don't have videos yet, you can create simple test videos:
```bash
# Create solid color test videos using ffmpeg
ffmpeg -f lavfi -i color=green:size=1920x1080:duration=5 -f lavfi -i sine=frequency=0:duration=5 videos/sleeping_face.mp4
ffmpeg -f lavfi -i color=red:size=1920x1080:duration=5 -f lavfi -i sine=frequency=0:duration=5 videos/angry_face.mp4
```

## Platform-Specific Setup

### macOS
```bash
# VLC installation
# Download from https://www.videolan.org/vlc/download-macosx.html

# Display detection
system_profiler SPDisplaysDataType  # Lists connected displays

# Camera permissions
# System Preferences > Security & Privacy > Camera > Enable for Terminal/Python
```

### Windows
```bash
# VLC installation  
# Download from https://www.videolan.org/vlc/download-windows.html

# Additional Windows packages (if needed)
pip install pywin32  # For display detection
```

### Linux
```bash
# VLC installation
sudo apt-get install vlc  # Ubuntu/Debian
sudo yum install vlc      # CentOS/RHEL

# Display detection
xrandr  # Lists connected displays
```

## Troubleshooting

### VLC Issues
- **"VLC not found"**: Install VLC from videolan.org
- **"No module named vlc"**: Run `pip install python-vlc`
- **Video won't play**: Check video file exists and is VLC-compatible
- **Black screen**: Try different video format or check VLC installation

### Display Issues
- **Wrong display**: Use `--list-displays` to find correct index
- **No fullscreen**: Check display is set as extended (not mirrored)
- **Video too small/large**: VLC automatically scales, check display resolution

### Camera Issues  
- **No camera detected**: Run `--list-cameras` to see available options
- **Wrong camera**: Try `--source 1`, `--source 2`, etc.
- **Permission denied**: Check camera permissions in system settings

### Performance Issues
- **Slow video switching**: Use lower resolution videos or faster storage
- **High CPU usage**: Lower YOLO confidence or reduce camera resolution
- **Stuttering video**: Check video encoding and hardware acceleration

## Advanced Configuration

### Multiple Hand Signs (Stretch Feature)
For future development, the system can be extended to recognize multiple hand signs:
```python
# Example classification mapping
sign_to_video = {
    'open_hand': 'videos/scare_1.mp4',
    'closed_fist': 'videos/scare_2.mp4', 
    'peace_sign': 'videos/scare_3.mp4',
    'thumbs_up': 'videos/special.mp4'
}
```

### Custom State Machine
The `VLCProjectionController` class can be extended for more complex behaviors:
- Multiple video sequences
- Timed transitions
- Audio integration
- Interactive modes

## Production Deployment

### Demo Day Checklist
- [ ] ✅ VLC installed and tested
- [ ] ✅ Videos created and placed in videos/ directory
- [ ] ✅ Projector connected and configured as extended display
- [ ] ✅ Camera positioned and tested
- [ ] ✅ Hand detection threshold calibrated
- [ ] ✅ Fullscreen projection tested on correct display
- [ ] ✅ Backup videos available
- [ ] ✅ Emergency stop procedure (Ctrl+C)

### Performance Optimization
- Use SSD storage for video files
- Close unnecessary applications
- Test with actual lighting conditions
- Calibrate detection threshold for environment

---

## Advantages Over Mapping Software

### Simplicity
- **No external software**: Just VLC (pre-installed on many systems)
- **No complex mapping**: Direct video file playback
- **No licensing**: Free and open source

### Reliability  
- **Fewer dependencies**: Less software to fail
- **Direct control**: Python controls VLC directly
- **Cross-platform**: Works on Mac, Windows, Linux

### Flexibility
- **Any video format**: VLC supports everything
- **Easy content updates**: Just replace video files
- **Custom behaviors**: Full programmatic control

This VLC-based approach provides a simpler, more reliable alternative to mapping software while maintaining all the core functionality needed for the Halloween hand detection projection system. 🎃