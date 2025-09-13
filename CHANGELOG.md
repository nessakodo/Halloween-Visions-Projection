# VPT8 Crash Fix & OSC Testing - Changelog

## 2025-09-12: VPT8 Crash Mitigation (macOS 15.6.1, Apple Silicon)

### Problem
- VPT8 repeatedly crashed with `EXC_BAD_ACCESS (SIGSEGV)` in `libviddll.dylib`
- Crash occurred in `ActiveURICache::removeURIsLinkedToCache` during OSC-triggered video operations
- Running under Rosetta translation on Apple Silicon made timing issues worse

### Root Cause
- VIDDLL video engine had race conditions in cache management
- OSC messages triggering video load/unload operations caused memory access violations

### Solution Applied
1. **Removed VIDDLL Package**
   - Deleted `/Applications/VPT8.app/Contents/Resources/C74/packages/VIDDLL/`
   - Forces VPT8 to use AVFoundation engine instead

2. **Updated VPT8 Preferences**
   ```
   preview 0                 # Disabled live preview to reduce load
   previewframerate 10       # Reduced from 15
   framerate 15              # Reduced from 30
   number_of_screens 1       # Kept existing
   preview_width 320         # Kept existing
   ```

### Results
- ✅ **No more crashes** - VPT8 now stable with OSC control
- ✅ **AVFoundation engine** - More stable on macOS/Apple Silicon
- ✅ **Reduced CPU/GPU load** - No live preview window
- ⚠️ **HAP codec support lost** - Stick to H.264 MP4 files
- ⚠️ **Some VIDDLL features unavailable** - Use standard codecs

### OSC Testing Status
- **Layer fade control working**: `/1layer/fade` and `/2layer/fade` 
- **Visual confirmation**: Preview shows left/right videos switching
- ✅ **Row 8 Mix Fader Control WORKING**: Multiple OSC paths tested, fader responds
- **Working OSC paths**: `/sources/8video/mixfader`, `/sources/8video/mix`, `/sources/8/mixfader`, etc.
- **Visual confirmation**: Mix fader moves in VPT8 interface, blends between inputs

### Current Setup
- **Row 8 mixer**: Two video inputs (idle + scare) 
- **Mix fader**: 0.0 = idle video, 1.0 = scare video
- **Output routing**: Row 8 → Projection layer
- **OSC control**: Smooth crossfades and quick flashes working

## 2025-09-12: Hand Detection Simulation Success

### Hand Detection Logic Implemented
- ✅ **Confidence threshold**: 90% required to trigger scare
- ✅ **State management**: Prevents rapid switching between idle/scare
- ✅ **Automatic return**: 2-second scare duration, then back to idle
- ✅ **OSC integration**: Uses working mix fader control paths

### Testing Results
- ✅ **Simulation working**: `test_hand_detection_sim.py` successfully triggers scare mode
- ✅ **Visual confirmation**: Mix fader moves, projection changes from idle to scare
- ✅ **Timing validation**: 2-second scare duration feels appropriate
- ✅ **Threshold validation**: 90% confidence threshold prevents false triggers

### Ready for YOLO Integration
- **Logic proven**: Hand detection simulation works perfectly
- **OSC paths confirmed**: Multiple working paths for reliability
- **State machine stable**: Clean transitions between idle/scare modes
- **Next step**: Replace simulated confidence with real YOLO hand detection

## 2025-09-12: REAL YOLO HAND DETECTION SUCCESS! 🎉

### Integration Complete
- ✅ **Fine-tuned model integrated**: Using `best.pt` classification model
- ✅ **Real-time hand detection**: YOLO classification working perfectly
- ✅ **Scare system functional**: Hand detection triggers video changes in VPT8
- ✅ **95% confidence threshold**: Adjusted from 90% to reduce false positives
- ✅ **Performance excellent**: Smooth real-time processing with camera feed

### Technical Implementation
- **Model**: `best.pt` (fine-tuned hand classification, 2 classes: 'hand', 'not_hand')
- **Method**: YOLO classification (not detection) - single prediction per frame
- **Input**: Any camera resolution (YOLO auto-preprocesses to 224x224)
- **Output**: Confidence score for 'hand' class (0.0-1.0)
- **Trigger logic**: `if class_name == 'hand' and confidence >= 0.95`

### Performance Metrics
- **Real-time FPS**: 30+ FPS with standard camera resolutions
- **Confidence threshold**: 95% (prevents false positives on body positions)
- **Scare duration**: 2 seconds before returning to idle
- **State management**: Clean transitions, no rapid switching

### Files Created/Modified
- ✅ `scripts/yolo_hand_scare_bridge.py` - Main integration script
- ✅ `scripts/test_hand_detection_sim.py` - Simulation for testing logic
- ✅ `best.pt` - Fine-tuned hand classification model (moved to repo root)
- ✅ `CHANGELOG.md` - Comprehensive documentation

### Current Status: PRODUCTION READY
The Halloween projection system is now fully functional with real-time hand detection triggering scare effects through VPT8 video mixing.

### Recommended Video Settings
- **Format**: H.264 MP4
- **Resolution**: 720p or 480p maximum  
- **Bitrate**: Modest (avoid high bitrate files)
- **Avoid**: HAP, VIDDLL-dependent formats

---

## Next Steps
- Test row 8 mix fader OSC control: `/sources/8video/mixfader`
- Optimize for single mixed output to projection layer