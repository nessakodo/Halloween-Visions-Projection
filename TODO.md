# TODO: Outstanding Tasks - VLC Direct Projection

## 🚀 High Priority

### Cross-Platform Testing
- [ ] **Windows VLC setup testing** - Verify python-vlc on Windows systems
  - Test VLC installation and python-vlc compatibility
  - Display detection and fullscreen projection
  - Camera permissions and driver compatibility
  - **Blocker**: Needs Windows machine for testing/verification

### Video Content
- [ ] **Create demo video files** - Test content for immediate use
  - `videos/sleeping_face.mp4` - Calm, ambient demo content
  - `videos/angry_face.mp4` - Scare, alert demo content
  - **Formats**: MP4 (H.264), 1080p recommended
  - **Duration**: 5-10 seconds, seamless loops

### Documentation
- [ ] **VLC installation screenshots** - Capture setup process for docs
  - `docs/images/vlc-installation-macos.png`
  - `docs/images/vlc-installation-windows.png`
  - `docs/images/display-setup-example.png`
  - `docs/images/projection-example.png`

## 🔧 Medium Priority

### Platform Optimization
- [ ] **Linux VLC support** - Test and document Linux setup
- [ ] **macOS display detection improvement** - Better multi-monitor support
- [ ] **Windows display enumeration** - Test win32api integration

### Features
- [ ] **Audio integration** - Add sound effects to video transitions
- [ ] **Video preview mode** - Small preview window for content verification
- [ ] **Configuration file** - Save/load projection settings
- [ ] **Performance monitoring** - FPS and resource usage display

### Testing
- [ ] **Automated VLC testing** - Unit tests for VLCProjectionController
- [ ] **Video format compatibility** - Test AVI, MOV, MKV formats
- [ ] **Error recovery testing** - Handle VLC crashes and restarts
- [ ] **Multi-display stress testing** - Extended display configurations

## 🎯 Low Priority

### Advanced Features
- [ ] **Multiple hand sign recognition** - Extend YOLO for sign language
  - Train model for open_hand, closed_fist, peace_sign, thumbs_up
  - Map different signs to different video content
  - Create sign → video mapping configuration

### Optimization
- [ ] **Video preloading** - Cache videos in memory for instant switching
- [ ] **GPU acceleration** - Leverage VLC hardware acceleration
- [ ] **Memory optimization** - Reduce footprint for long sessions
- [ ] **Startup time improvement** - Faster initialization

### User Experience
- [ ] **Web interface** - Simple web UI for non-technical users
- [ ] **Mobile monitoring** - Remote monitoring via phone/tablet
- [ ] **Voice commands** - Basic voice control integration
- [ ] **Gesture calibration** - Interactive threshold adjustment

### Development Tools
- [ ] **Video content creator** - Tool to generate test videos
- [ ] **Projection simulator** - Test without physical projector
- [ ] **Performance profiler** - Optimize YOLO + VLC performance

## 📝 Notes

### Video Content Guidelines
- **Recommended Format**: MP4 (H.264 codec)
- **Resolution**: 1920x1080 (scales automatically)
- **Duration**: 3-10 seconds for seamless looping
- **Content Types**:
  - Idle: Calm faces, ambient scenes, gentle movements
  - Scare: Jump scares, scary faces, sudden movements

### Testing Requirements
- **VLC Installation**: Required on all test platforms
- **python-vlc**: Must work with local VLC installation
- **Multi-display**: Test with actual projector setup
- **Performance**: Maintain 30+ FPS with video switching

### Community Contributions Welcome
- **Video content creation** - Halloween-themed videos
- **Cross-platform testing** - Windows and Linux verification  
- **Documentation improvements** - Setup guides and troubleshooting
- **Feature development** - Hand sign recognition, audio integration

## ✅ Recently Completed

- [x] **VLC direct projection implementation** - Core video switching system
- [x] **YOLO hand detection integration** - 99% confidence threshold
- [x] **Multi-display support** - Fullscreen projection targeting
- [x] **Cross-platform foundation** - macOS, Windows, Linux compatibility
- [x] **Video directory structure** - Organized content management
- [x] **Testing utilities** - VLC validation and debugging tools
- [x] **Comprehensive documentation** - Setup guides and troubleshooting
- [x] **Repository cleanup** - Removed mapping software dependencies

## 🔮 Future Roadmap

### Phase 1: Stability (Current)
- Complete cross-platform testing
- Create demo video content
- Finalize documentation with screenshots

### Phase 2: Enhancement
- Multiple hand sign recognition
- Audio integration
- Advanced video effects

### Phase 3: Advanced Features
- Web interface for control
- Mobile app integration
- AI-generated content

---

## 🎯 Demo Day Priorities

**Critical for Halloween Demo:**
1. ✅ VLC projection working reliably
2. ✅ Hand detection calibrated for lighting
3. ✅ Video content created and tested
4. ✅ Projector setup documented and tested
5. ✅ Emergency procedures defined

**Nice to Have:**
- Multiple video variations for variety
- Audio effects for enhanced scares
- Backup projection method

---

*Last updated: 2025-09-22 - VLC Direct Projection Focus*