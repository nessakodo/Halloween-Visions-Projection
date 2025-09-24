# 🎃 Halloween Hand Detection Workshop

**Build a spooky projection system that reacts to trick-or-treaters!**

---

## 🚀 WORKSHOP SETUP (Do This First!)

### Step 1: Install Requirements

**Install Git LFS** (required for model and video files):
```bash
# macOS
brew install git-lfs

# Ubuntu/Debian  
sudo apt install git-lfs

# Windows: Download from git-lfs.github.io
```

### Step 2: Get the Code & Setup Environment
```bash
git clone https://github.com/12mv2/Halloween-Visions-Projection.git
cd Halloween-Visions-Projection
git lfs pull  # Downloads the AI model and video files

# Create virtual environment (keeps your system clean!)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies in the virtual environment
pip install -r requirements.txt
```

**💡 Remember:** Always run `source venv/bin/activate` before using the system!

### Step 3: Test It Works
```bash
python simple_projection.py --source 0 --conf 0.5
```

**✅ Success Check:** You should see:
- A window with your camera feed
- Hand detection confidence numbers updating
- Video switching when you wave your hands

**🎮 Controls:**
- **D** = Toggle Debug/Clean mode  
- **F** = Fullscreen
- **Q** or **ESC** = Quit

---

## 🎯 Workshop Activities

### Activity 1: Basic Hand Detection Test
1. Run the system with your camera
2. Wave your hands - watch the confidence scores
3. See the video switch from idle to scare mode
4. Experiment with different confidence levels:
   ```bash
   python simple_projection.py --source 0 --conf 0.3  # More sensitive
   python simple_projection.py --source 0 --conf 0.7  # Less sensitive
   ```

### Activity 2: Customize Your Videos
1. **Find your videos:** `sleeping_face.mp4` (idle) and `angry_face.mp4` (scare)
2. **Replace with your own:**
   ```bash
   python simple_projection.py --video-sleep YOUR_IDLE.mp4 --video-scare YOUR_SCARE.mp4
   ```
3. **Test the new experience**

### Activity 3: Halloween Production Setup
1. **Connect projector** to your laptop
2. **Run the system:**
   ```bash
   python simple_projection.py --source 0 --conf 0.5 --fullscreen
   ```
3. **Switch to clean mode:** Press **D** (no debug info)
4. **Position camera** to detect approaching trick-or-treaters
5. **Test and scare!** 🎃

---

## 🛠️ If Something Goes Wrong

### Camera Not Working?
```bash
# Try different camera
python simple_projection.py --source 1

# Check camera permissions
# macOS: System Preferences → Privacy & Security → Camera
```

### Hand Detection Not Sensitive Enough?
```bash
# Lower the confidence threshold
python simple_projection.py --source 0 --conf 0.3
```

### Videos Not Playing?
- Check that Git LFS pulled the files: `ls -la *.mp4`
- If missing: `git lfs pull`

---

## 🎬 How It Works (The Magic Behind It)

1. **Camera** captures live video of trick-or-treaters approaching
2. **AI Model** (YOLO) classifies each frame as 'hand detected' or 'no hand'
3. **Video Player** switches instantly between idle and scare videos
4. **Projector** displays the spooky experience

### 🖐️ Hand Detection Details
- **Model:** `Colin1.pt` - trained YOLO classification model
- **Classes:** `{0: 'hand', 1: 'not_hand'}`
- **Real-time:** 30+ FPS processing
- **Smart logic:** 2-second scare duration with debounce

### 🎥 Video System
- **OpenCV-powered** for reliable playback
- **Instant switching** between videos
- **Any format** supported by OpenCV
- **Fullscreen projection** ready

---

## 📚 Advanced Features & Configuration

### Command Line Options
```bash
python simple_projection.py [OPTIONS]

--source 0                # Camera index (0=USB, 1=built-in)
--conf 0.5               # Hand detection confidence (0.3-0.9)
--video-sleep PATH       # Custom idle video path
--video-scare PATH       # Custom scare video path
--fullscreen            # Start in fullscreen mode
```

### System Requirements
- **macOS/Linux/Windows** (tested on macOS Darwin 24.6.0)
- **Python 3.11+**
- **Git LFS** (for model and video files)
- **USB camera** or built-in camera
- **Projector** or external display

### Dependencies
- `ultralytics>=8.0.0` - YOLO model inference
- `opencv-python>=4.0.0` - Video processing and display
- `python-vlc>=3.0.0` - VLC integration (legacy)

### Production Tips
- **USB camera recommended** - works with laptop lid closed
- **Detection range:** 3-6 feet optimal
- **Lighting:** Ensure adequate lighting for AI accuracy
- **Mirrored displays:** System Preferences → Displays → Mirror

---

## 🎃 Production Status

**✅ WORKSHOP READY!**
- ✅ Hand detection: Accurate and responsive  
- ✅ Video switching: Smooth and instant
- ✅ Multi-camera support: USB + built-in tested
- ✅ Cross-platform: macOS/Linux/Windows

**⚠️ Known Issue:** Grey border at display top (macOS OpenCV limitation)  
**Workaround:** Position projector to crop the border area

---

**🎃 Ready to create some Halloween magic! 👻**

*Workshop complete? Share your spooky creation and help improve this project!*
*Special thanks to the ML Vision Projects Halloween crew for their help*