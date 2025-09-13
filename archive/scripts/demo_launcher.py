#!/usr/bin/env python3
"""
Halloween Projection Mapping - Demo Launcher
Interactive launcher for quick demo setup
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_venv():
    """Check if we're running in virtual environment"""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

def run_command(cmd, description):
    """Run a command and show result"""
    print(f"\n{description}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✓ {description} successful")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {description} failed")
            print(f"Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⚠ {description} timed out")
        return False
    except Exception as e:
        print(f"✗ {description} error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Halloween Projection Demo Launcher")
    parser.add_argument("--skip-tests", action="store_true", help="Skip dependency tests")
    parser.add_argument("--model", default="yolov8n.pt", help="YOLO model to use")
    parser.add_argument("--source", default="0", help="Camera source")
    parser.add_argument("--conf", type=float, default=0.6, help="Confidence threshold")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    print("🎃 Halloween Projection Mapping - Demo Launcher")
    print("=" * 50)
    
    # Check virtual environment
    if not check_venv():
        print("⚠ Warning: Not running in virtual environment")
        print("  Run: source .venv/bin/activate")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return 1
    else:
        print("✓ Virtual environment active")
    
    # Check project structure
    required_files = [
        "scripts/yolo_vpt_bridge.py",
        "scripts/test_dependencies.py",
        "scripts/test_osc_vpt.py",
        "media/idle.mp4",
        "media/scare.mp4",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        print("  Run: python scripts/create_test_media.py")
        return 1
    else:
        print("✓ All required files present")
    
    # Run tests unless skipped
    if not args.skip_tests:
        print("\n" + "=" * 50)
        print("Running System Tests")
        print("=" * 50)
        
        # Test dependencies
        success = run_command(
            [sys.executable, "scripts/test_dependencies.py"],
            "Testing dependencies"
        )
        
        if not success:
            print("⚠ Some dependency tests failed - continuing anyway")
        
        # Test OSC
        print("\nℹ For OSC test: Make sure VPT is running with OSC enabled")
        response = input("Run OSC test? (Y/n): ")
        if response.lower() != 'n':
            run_command(
                [sys.executable, "scripts/test_osc_vpt.py"],
                "Testing OSC communication"
            )
    
    # Launch demo
    print("\n" + "=" * 50)
    print("Launching Demo")
    print("=" * 50)
    
    print(f"Model: {args.model}")
    print(f"Source: {args.source}")
    print(f"Confidence: {args.conf}")
    print(f"Debug mode: {args.debug}")
    
    # Build command
    cmd = [
        sys.executable, 
        "scripts/yolo_vpt_bridge.py",
        "--model", args.model,
        "--source", args.source,
        "--conf", str(args.conf),
        "--show"
    ]
    
    if args.debug:
        cmd.append("--debug")
    
    print(f"\nCommand: {' '.join(cmd)}")
    print("\n🎯 Demo Instructions:")
    print("1. Make sure VPT is running with OSC enabled")
    print("2. Position yourself in front of the camera")
    print("3. Wave or move to trigger detection")
    print("4. Press ESC or Q to quit, Ctrl+C to stop")
    print("\nPress Enter to start demo...")
    input()
    
    try:
        # Run the demo directly (not captured)
        os.execv(sys.executable, cmd)
    except KeyboardInterrupt:
        print("\n\nDemo stopped by user")
        return 0
    except Exception as e:
        print(f"\n\nDemo failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())