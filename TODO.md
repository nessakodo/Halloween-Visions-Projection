# TODO: Outstanding Tasks

## 🚀 High Priority

### Windows Support
- [ ] **Windows setup documentation** - Create `docs/DEMO_SETUP_WINDOWS.md`
  - HeavyM Windows version compatibility testing
  - Python environment setup (venv vs conda)
  - Camera permissions and drivers
  - MIDI library compatibility (python-rtmidi on Windows)
  - **Blocker**: Needs Windows machine for testing/verification

### Documentation
- [ ] **HeavyM configuration screenshots** - Capture and add to `docs/images/`
  - `heavym-midi-setup.png` - MIDI input configuration
  - `heavym-sequence-creation.png` - Creating sleepseq and scareseq
  - `heavym-midi-learning.png` - MIDI Learning mode setup
  - `heavym-sequence-mapping.png` - Note 60/61 mapping verification

## 🔧 Medium Priority

### Platform Testing
- [ ] **M1 chip compatibility** - Test MIDI bridge on Apple Silicon
- [ ] **Linux support investigation** - Research HeavyM alternatives or MIDI compatibility

### Features
- [ ] **Camera auto-discovery improvement** - Better USB camera detection
- [ ] **Configuration file** - Save/load camera and MIDI settings
- [ ] **Web interface** - Simple web UI for non-technical users
- [ ] **MIDI device selection** - Choose specific MIDI output ports

## 🎯 Low Priority

### Optimization
- [ ] **Performance profiling** - Optimize YOLO inference speed
- [ ] **Memory usage** - Reduce footprint for longer sessions
- [ ] **Error recovery** - Auto-reconnect on camera/MIDI failures

### MIDI Enhancements
- [ ] **MIDI channel selection** - Support different MIDI channels
- [ ] **CC message support** - Alternative to note on/off messages
- [ ] **MIDI monitoring** - Real-time MIDI message display

### Documentation
- [ ] **Video tutorials** - Screen recordings of HeavyM + MIDI setup
- [ ] **Troubleshooting guide** - Common MIDI and HeavyM issues
- [ ] **Architecture documentation** - Technical deep-dive on MIDI bridge

## 📝 Notes

- **Windows testing**: Need volunteer with Windows machine and HeavyM
- **Screenshots**: Can be captured during next HeavyM session
- **Community contributions welcome** - See individual tasks for requirements
- **MIDI compatibility**: Tested on macOS, Windows/Linux need verification

## ✅ Recently Completed

- [x] **HeavyM MIDI integration** - Replace VPT8 OSC with MIDI bridge
- [x] **Demo version compatibility** - Works with free HeavyM Demo
- [x] **macOS MIDI setup** - IAC Driver integration and documentation
- [x] **Documentation overhaul** - Updated all docs from VPT8 to HeavyM
- [x] **Test utilities** - MIDI testing and setup scripts

---

*Last updated: 2025-09-21*