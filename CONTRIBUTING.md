# Contributing to Halloween Hand Detection Projection System

Thank you for your interest in contributing! This project brings Halloween projections to life with real-time hand detection, and we welcome contributions from developers at all experience levels.

## Getting Started

### Quick Setup
1. **Fork this repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/Halloween-Visions.git
   cd Halloween-Visions
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Understanding the Project
- **Core functionality**: YOLO hand detection triggers scare effects in VPT8 projection mapping
- **Tech stack**: Python, OpenCV, YOLO, OSC, VPT8
- **Target users**: Artists, makers, and Halloween enthusiasts

## Development Workflow

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** with a descriptive name:
   ```bash
   git checkout -b add-windows-documentation
   git checkout -b fix-camera-detection
   git checkout -b improve-error-messages
   ```
4. **Make your changes** following our coding standards
5. **Test thoroughly** on your platform
6. **Commit your changes** with clear messages
7. **Push to your fork**: `git push origin your-branch-name`
8. **Create a Pull Request** with:
   - Clear title describing what you did
   - Detailed description of changes made
   - Any testing performed
   - Screenshots if applicable (especially for documentation)

## Good First Issues

Check our [TODO.md](TODO.md) for tasks marked by priority. Here are some beginner-friendly areas:

**Documentation** (No coding required):
- Capture VPT8 configuration screenshots
- Write Windows setup documentation  
- Create troubleshooting guides

**Testing & Verification**:
- Test on different platforms (M1 Mac, Windows, Linux)
- Verify camera compatibility with various USB cameras
- Test VPT8 versions and document compatibility

**Code Improvements**:
- Enhance error messages and user feedback
- Add configuration file support
- Improve camera auto-discovery

## Code Standards

- **Python**: Follow PEP 8 styling
- **Comments**: Document complex logic and hardware interactions
- **Error handling**: Provide helpful error messages with next steps
- **Testing**: Include tests for new functionality when possible

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create an issue with reproduction steps
- **Feature requests**: Check TODO.md first, then open an issue

## Recognition

All contributors will be acknowledged in our README and release notes. First-time contributors receive special recognition for helping grow our community.

---

Ready to contribute? Check out our [current TODO items](TODO.md) and find something that matches your interests and skills!