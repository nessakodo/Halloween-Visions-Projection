# DEMO_SETUP.md

## 🎃 Quick Setup (5–10 minutes)

### 0) Prerequisites
**Git LFS** (required for video files):
```bash
git lfs install
```

**VPT8 Download:**
Download VPT8 Mac version (Intel build) from the official website. **Do not use** the Silicon beta version.

### 1) Environment setup (virtualenv)
```bash
# Navigate to your project directory
cd /path/to/Halloween-Visions

# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
To leave the venv later: `deactivate`

### 2) VPT8 version (critical)
- ✅ Use **VPT8 Mac version** (Intel build under Rosetta) - Mix module works
- ❌ **Do not use** VPT8 Silicon beta (Mix module broken) - applies to M2+ chips
- ❓ **M1 chip compatibility** - not tested, use Intel build to be safe

### 3) VPT8 crash prevention
Remove the VIDDLL package (we removed it, not just renamed):

**Option 1 (Terminal):**
```bash
rm -rf /Applications/VPT8.app/Contents/Resources/C74/packages/VIDDLL
```

**Option 2 (Finder - if you prefer GUI):**
1. Open Finder
2. Navigate to Applications → VPT8.app → Show Package Contents
3. Go to Contents → Resources → C74 → packages
4. Delete the VIDDLL folder
Recommended project prefs (in your project's `prefs.txt`):
```
preview 0
previewframerate 10
framerate 15
```

### 4) VPT8 configuration

**VPT8 Window Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│ VPT8 WINDOW                                                     │
├─────────────────────────────┬───────────────────────────────────┤
│ LEFT PANEL                  │ RIGHT PANEL (Sources)             │
│                             │                                   │
│ 🎛️ Active Inspector:         │ Row 1: [1video] ← Video A        │
│   - Layer settings          │ Row 2: [2video] ← Video B        │
│   - Source: 8video          │ Row 8: [8mix] ← A/B Crossfader   │
│   - Fade: 1.0              │                                   │
│                             │ ──────────────────────────────── │
│ 📺 Preview Window:          │ Layer: [gulvtekstur] ← Your layer│
│   Shows final output        │                                   │
│                             │                                   │
├─────────────────────────────┴───────────────────────────────────┤
│ BOTTOM BAR: blackout OFF | masterlevel > 0                     │
└─────────────────────────────────────────────────────────────────┘
```

**Sources (right column):**
- Row 1 = `1video` → load idle video → On + Loop
- Row 2 = `2video` → load scare video → On + Loop
- Row 8 = `mix` → On → **A=1video**, **B=2video**, **mode=mix**

*📸 Screenshot needed: VPT8 row 8 mix setup (save as docs/images/vpt8-row8-mix-setup.png)*


**Layer (active inspector):**
- Select your layer (e.g., `layer_1` / `gulvtekstur`)
- **Source = 8video**
- **fade = 1.0**
- Bottom bar: **blackout off**, masterlevel > 0

*📸 Screenshot needed: VPT8 layer configuration (save as docs/images/vpt8-layer-config.png)*


**Note:** With the working Intel build, the **row 8 mix thumbnail is reliable** and tracks the mix slider.

*📸 Screenshot needed: VPT8 mix thumbnail showing crossfade (save as docs/images/vpt8-mix-thumbnail.png)*


### 5) OSC settings
**VPT8 OSC Configuration:**
- Open VPT8 → **osc** tab 
- Set **receive port = 6666**
- Enable **Monitor in** to see incoming messages

*📸 Screenshot needed: VPT8 OSC monitor showing incoming messages (save as docs/images/vpt8-osc-monitor.png)*

**What the bridge sends to VPT8:**
```bash
# Priming commands (sent once on startup)
/sources/1video/on 1
/sources/2video/on 1
/sources/8mix/on 1

# Crossfade commands (sent during hand detection)
/sources/8mix/mix 0.0   # Idle state (show video A)
/sources/8mix/mix 1.0   # Scare state (show video B)
```
The bridge sends float values 0.0–1.0 to smoothly crossfade between videos.

### 6) Test + run
```bash
# Test OSC
python scripts/test_osc_vpt.py

# Optional sim
python scripts/test_hand_detection_sim.py

# Production
python scripts/yolo_hand_scare_bridge.py        # or --show for preview
```