# 🎃 Halloween Hand Detection Projection System

**Simple, reliable projection system using OpenCV for direct video display**

## 🚀 Quick Start - Ready for Halloween!

### 1. Run the System
```bash
cd /Users/colinrooney/Dev/Active\ Projects/workshops/halloween/Halloween-Visions-Projection
python simple_projection.py --source 0 --conf 0.5
```

### 2. Controls
- **D** = Toggle Debug/Projection mode  
- **P** = Production mode (grey border fix attempt)
- **F** = Fullscreen toggle
- **Q** or **ESC** = Quit

### 3. Halloween Setup
1. **Test**: Run command above in debug mode
2. **Production**: Press **D** for clean projection mode
3. **Fullscreen**: Press **F** for fullscreen display
4. **Mirror to projector**: Use System Preferences → Displays → Mirror Displays

## 🎬 How It Works

1. **Camera** captures real-time video feed (USB or built-in)
2. **YOLO model** classifies entire frame as 'hand' or 'not_hand' 
3. **OpenCV window** switches between idle and scare videos instantly
4. **Projector display** shows seamless video switching for trick-or-treaters

## ✨ Key Features

### 🖐️ Hand Detection
- **Trained YOLO classification model** (best.pt) for accurate hand detection
- **50-99% confidence range** with real-time updates
- **Debounce logic** prevents video flickering
- **2-second scare duration** with automatic return to idle

### 🎥 Direct Video Display  
- **OpenCV-powered** - simple and reliable
- **Instant video switching** between sleeping_face.mp4 and angry_face.mp4
- **Fullscreen projection** support
- **Multi-mode display**: Debug (with camera feed + info) or clean projection
- **Any video format** supported by OpenCV

### 📷 Camera Support
- **USB external camera** (Camera 0) - works with laptop lid closed
- **Built-in laptop camera** (Camera 1) - when lid is open
- **Automatic initialization** with USB camera retry logic
- **Live preview** in debug mode

## ⚙️ Configuration

### Command Line Options
```bash
python simple_projection.py [OPTIONS]

--source 0                # Camera index (0=USB, 1=built-in)
--conf 0.5               # Hand detection confidence (0.3-0.9)
--video-sleep PATH       # Custom idle video path
--video-scare PATH       # Custom scare video path
--fullscreen            # Start in fullscreen mode
```

### Example Commands
```bash
# Basic usage
python simple_projection.py --source 0 --conf 0.5

# High sensitivity
python simple_projection.py --source 0 --conf 0.3

# Start fullscreen
python simple_projection.py --source 0 --conf 0.5 --fullscreen

# Use built-in camera 
python simple_projection.py --source 1 --conf 0.5
```

## 🎃 Halloween Production Setup

### Recommended Workflow
1. **Connect projector** to laptop (HDMI Etc.)
2. **Set up mirrored display** (System Preferences → Displays)
3. **Run projection system**:
   ```bash
   python simple_projection.py --source 0 --conf 0.5
   ```
4. **Configure for projection**:
   - Press **D** to switch to clean projection mode  
   - Press **F** for fullscreen
   - Position camera to detect approaching trick-or-treaters
5. **Test hand detection** - wave hands to trigger scare mode

### Camera Positioning
- **USB camera**: Position facing trick-or-treaters approach path
- **Detection range**: 3-6 feet optimal for hand detection
- **Lighting**: Ensure adequate lighting for YOLO model accuracy

## 🛠️ Technical Details

### System Requirements
- **macOS** (tested on Darwin 24.6.0 / Sequoia 15.6.1)
- **Python 3.11+**
- **Git LFS** (for model and video files)
- **VLC Media Player** (installed separately)
- **USB camera** or built-in camera
- **Projector** or external display

### Installation
1. **Install Git LFS** (required for model and video files):
   ```bash
   # macOS
   brew install git-lfs
   
   # Ubuntu/Debian  
   sudo apt install git-lfs
   
   # Windows: Download from git-lfs.github.io
   ```

2. **Clone repository with LFS files**:
   ```bash
   git clone https://github.com/12mv2/Halloween-Visions-Projection.git
   cd Halloween-Visions-Projection
   git lfs pull  # Download LFS files (Colin1.pt, videos)
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
- `ultralytics>=8.0.0` - YOLO model inference
- `opencv-python>=4.0.0` - Video processing and display
- `python-vlc>=3.0.0` - VLC integration (legacy system)

### Model Details
- **File**: `Colin1.pt` (trained YOLO classification model)
- **Classes**: `{0: 'hand', 1: 'not_hand'}`
- **Input**: Camera frame (any resolution)
- **Output**: Classification confidence (0.0-1.0)

## 🚨 Troubleshooting

### Camera Issues
```bash
# List available cameras
python simple_projection.py --list-cameras

# Try different camera index
python simple_projection.py --source 1

# Check permissions in System Preferences → Privacy & Security → Camera
```

### Detection Issues
```bash
# Lower confidence threshold
python simple_projection.py --source 0 --conf 0.3

# Check lighting conditions
# Ensure hands are clearly visible to camera
```

### Display Issues
- **Grey border at top**: Known OpenCV/macOS limitation, doesn't affect projector output

## 📊 Performance Notes

- **Hand detection**: 30+ FPS real-time processing
TODO - Test on different hardware

## 🎯 Production Status

**🎃 READY FOR HALLOWEEN (with workaround)**
- Core functionality: 100% working
- Hand detection: Accurate and responsive  
- Video switching: Functional
- Camera support: Multi-camera tested
TODO - Projection: Compatible with all projectors ???

**⚠️ Known Issue**: Grey border at top of display (see CONTRIBUTING.md for TODO)
**Workaround**: Position projector to crop grey area

---

**🎃 Ready to scare some trick-or-treaters! 👻**

