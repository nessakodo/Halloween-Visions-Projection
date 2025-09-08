#!/usr/bin/env python3
"""
Test script to verify all dependencies work correctly
"""

import sys
import traceback

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics YOLO imported successfully")
    except ImportError as e:
        print(f"✗ Ultralytics import failed: {e}")
        return False
    
    try:
        from pythonosc.udp_client import SimpleUDPClient
        print("✓ python-osc imported successfully")
    except ImportError as e:
        print(f"✗ python-osc import failed: {e}")
        return False
    
    return True

def test_yolo_model():
    """Test YOLO model loading with built-in model"""
    print("\nTesting YOLO model loading...")
    
    try:
        from ultralytics import YOLO
        
        # Use YOLOv8 nano model (will download automatically if needed)
        model = YOLO("yolov8n.pt")
        print("✓ YOLO model loaded successfully")
        
        # Test model info
        print(f"✓ Model classes: {len(model.names)} classes")
        print(f"✓ Sample classes: {list(model.names.values())[:5]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ YOLO model loading failed: {e}")
        traceback.print_exc()
        return False

def test_osc_client():
    """Test OSC client creation"""
    print("\nTesting OSC client...")
    
    try:
        from pythonosc.udp_client import SimpleUDPClient
        
        # Create OSC client (don't send messages yet)
        client = SimpleUDPClient("127.0.0.1", 6666)
        print("✓ OSC client created successfully")
        return True
        
    except Exception as e:
        print(f"✗ OSC client creation failed: {e}")
        return False

def test_camera():
    """Test camera access"""
    print("\nTesting camera access...")
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✓ Camera accessible, frame shape: {frame.shape}")
                cap.release()
                return True
            else:
                print("✗ Camera opened but couldn't read frame")
                cap.release()
                return False
        else:
            print("✗ Could not open camera")
            return False
            
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("Halloween Projection Mapping - Dependency Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("YOLO Model Test", test_yolo_model),
        ("OSC Client Test", test_osc_client),
        ("Camera Test", test_camera),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 20)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✓ All tests passed! System ready for demo.")
        return 0
    else:
        print("\n✗ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())