# TODO: Outstanding Tasks

## 🚀 High Priority

### Windows Support
- [ ] **Windows setup documentation** - Create `docs/DEMO_SETUP_WINDOWS.md`
  - VPT8 Windows version compatibility testing
  - Python environment setup (venv vs conda)
  - Camera permissions and drivers
  - OSC library compatibility
  - **Blocker**: Needs Windows machine for testing/verification

### Documentation
- [ ] **VPT8 configuration screenshots** - Capture and add to `docs/images/`
  - `vpt8-row8-mix-setup.png` - Sources panel showing mix configuration
  - `vpt8-layer-config.png` - Layer inspector with source=8video
  - `vpt8-mix-thumbnail.png` - Mix thumbnail showing crossfade
  - `vpt8-osc-monitor.png` - OSC monitor showing incoming messages

## 🔧 Medium Priority

### Platform Testing
- [ ] **M1 chip compatibility** - Test VPT8 Intel build under Rosetta on M1
- [ ] **Linux support investigation** - Research VPT8 alternatives or Wine compatibility

### Features
- [ ] **Camera auto-discovery improvement** - Better USB camera detection
- [ ] **Configuration file** - Save/load camera and OSC settings
- [ ] **Web interface** - Simple web UI for non-technical users

## 🎯 Low Priority

### Optimization
- [ ] **Performance profiling** - Optimize YOLO inference speed
- [ ] **Memory usage** - Reduce footprint for longer sessions
- [ ] **Error recovery** - Auto-reconnect on camera/OSC failures

### Documentation
- [ ] **Video tutorials** - Screen recordings of setup process
- [ ] **Troubleshooting guide** - Common issues and solutions
- [ ] **Architecture documentation** - Technical deep-dive

## 📝 Notes

- **Windows testing**: Need volunteer with Windows machine and VPT8 license
- **Screenshots**: Can be captured during next VPT8 session
- **Community contributions welcome** - See individual tasks for requirements

---

*Last updated: 2025-09-18*