#!/usr/bin/env python3
"""
YOLO Hand Detection → VPT8 Scare System
- Real-time hand detection using YOLO
- 90% confidence threshold for scare trigger
- Row 8 mix fader control (idle ↔ scare)
- Based on proven simulation logic
"""

import argparse
import time
import logging
import threading
from ultralytics import YOLO
from pythonosc.udp_client import SimpleUDPClient
import cv2

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

def list_available_cameras():
    """Detect and list available cameras"""
    available_cameras = []
    
    print("🔍 Scanning for available cameras...")
    
    for index in range(6):  # Check camera indices 0-5
        try:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    height, width = frame.shape[:2]
                    available_cameras.append({
                        'index': index,
                        'resolution': f"{width}x{height}",
                        'status': 'Working'
                    })
                    print(f"  📷 Camera {index}: {width}x{height} - ✅ Working")
                else:
                    print(f"  📷 Camera {index}: ❌ Can't read frames")
                cap.release()
            # Don't show failed cameras to reduce noise
        except Exception:
            # Handle any camera access errors silently
            pass
    
    if not available_cameras:
        print("  ❌ No working cameras found")
        print("\n💡 Troubleshooting:")
        print("     • Check camera permissions in System Preferences")
        print("     • Ensure no other app is using cameras")
        print("     • Try unplugging/replugging USB cameras")
    else:
        print(f"\n✅ Found {len(available_cameras)} working camera(s)")
        print("\nUsage examples:")
        for cam in available_cameras:
            if cam['index'] == 0:
                print(f"  # Use built-in camera (default)")
                print(f"  python scripts/yolo_hand_scare_bridge.py --show")
            else:
                print(f"  # Use external camera {cam['index']}")
                print(f"  python scripts/yolo_hand_scare_bridge.py --source {cam['index']} --show")
    
    return available_cameras

class HandScareController:
    def __init__(self, vpt_host="127.0.0.1", vpt_port=6666):
        self.client = SimpleUDPClient(vpt_host, vpt_port)
        self.lock = threading.Lock()
        
        # Scare system parameters
        self.state = "idle"  # "idle" or "scare"
        self.confidence_threshold = 0.99  # 99% confidence required
        self.scare_duration = 0.0  # seconds to stay in scare mode
        self.last_trigger = 0.0
        
        logging.info(f"HandScareController initialized")
        logging.info(f"Confidence threshold: {self.confidence_threshold:.0%}")
        logging.info(f"Scare duration: {self.scare_duration}s")
        
    def set_mix_fader(self, value):
        """Control the row 8 mix fader (0.0=idle, 1.0=scare)"""
        with self.lock:
            # Use all the proven working OSC paths
            self.client.send_message("/sources/8video/mixfader", float(value))
            self.client.send_message("/sources/8video/mix", float(value))
            self.client.send_message("/sources/8/mixfader", float(value))
            self.client.send_message("/sources/8/mix", float(value))
            self.client.send_message("/8video/mixfader", float(value))
            self.client.send_message("/8video/mix", float(value))
    
    def process_classification(self, result):
        """Process YOLO classification result and trigger scare if hand detected with high confidence"""
        now = time.time()
        
        # Get classification results
        confidence = result.probs.top1conf.item()  # 0.0 to 1.0
        class_name = result.names[result.probs.top1]  # 'hand' or 'not_hand'
        
        # State machine logic
        if class_name == 'hand' and confidence >= self.confidence_threshold and self.state != "scare":
            logging.info(f"🖐️  HAND DETECTED! Confidence: {confidence:.1%}")
            logging.info("   → Triggering SCARE mode")
            self.set_mix_fader(1.0)  # Switch to scare video
            self.state = "scare"
            self.last_trigger = now
            
        elif self.state == "scare" and (now - self.last_trigger) >= self.scare_duration:
            logging.info("   → SCARE timeout, returning to IDLE mode")
            self.set_mix_fader(0.0)  # Switch back to idle
            self.state = "idle"
        
        return {
            'confidence': confidence,
            'class_name': class_name,
            'state': self.state
        }

def parse_args():
    p = argparse.ArgumentParser(description="YOLO Hand Detection → VPT8 Scare System")
    p.add_argument("--model", default="best.pt", help="YOLO model file (hand detection models in models/hand-detection/)")
    p.add_argument("--source", default=0, help="Camera index (0=built-in, 1=external, etc.) or video file")
    p.add_argument("--list-cameras", action="store_true", help="List available cameras and exit")
    p.add_argument("--conf", type=float, default=0.5, help="YOLO detection confidence (lower = more detections)")
    p.add_argument("--scare-conf", type=float, default=0.90, help="Confidence threshold for scare trigger")
    p.add_argument("--scare-duration", type=float, default=2.0, help="Scare duration in seconds")
    p.add_argument("--vpt-host", default="127.0.0.1", help="VPT8 host")
    p.add_argument("--vpt-port", type=int, default=6666, help="VPT8 OSC port")
    p.add_argument("--show", action="store_true", help="Show video window with detections")
    p.add_argument("--debug", action="store_true", help="Enable debug logging")
    return p.parse_args()

def main():
    args = parse_args()
    
    # Handle camera listing
    if args.list_cameras:
        list_available_cameras()
        return 0
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logging.info("=" * 60)
    logging.info("YOLO Hand Detection → VPT8 Scare System")
    logging.info("=" * 60)
    
    # Load YOLO model
    try:
        logging.info(f"Loading YOLO model: {args.model}")
        model = YOLO(args.model)
        logging.info(f"✓ Model loaded: {len(model.names)} classes available")
        
        # Check model classes (should be {0: 'hand', 1: 'not_hand'})
        logging.info(f"✓ Model classes: {model.names}")
        if 'hand' in model.names.values():
            logging.info("✓ Hand classification model detected")
        else:
            logging.warning("⚠️  Expected 'hand' class not found in model")
            
    except Exception as e:
        logging.error(f"Failed to load YOLO model: {e}")
        return 1
    
    # Initialize scare controller
    controller = HandScareController(args.vpt_host, args.vpt_port)
    controller.confidence_threshold = args.scare_conf
    controller.scare_duration = args.scare_duration
    
    # Start in idle state
    logging.info("Starting in IDLE state...")
    controller.set_mix_fader(0.0)
    time.sleep(1)
    
    # Set up video source - ensure camera index is integer
    try:
        src = int(args.source)
        logging.info(f"Camera source: {src}")
    except ValueError:
        src = args.source
        logging.info(f"Video file source: {src}")
        
    logging.info(f"YOLO confidence: {args.conf}")
    logging.info(f"Scare confidence: {args.scare_conf:.0%}")
    logging.info("Press 'q' or ESC to quit (when --show enabled), or Ctrl+C")
    logging.info("-" * 60)
    
    frame_count = 0
    
    try:
        # For classification, we need to process frames one by one
        import cv2 as cv_capture
        cap = cv_capture.VideoCapture(src)
        
        if not cap.isOpened():
            logging.error(f"❌ Could not open camera/video source: {src}")
            
            # Try fallback cameras if using camera index
            if isinstance(src, int) and src != 0:
                logging.info("🔄 Attempting fallback to built-in camera (index 0)...")
                cap = cv_capture.VideoCapture(0)
                if cap.isOpened():
                    logging.warning("⚠️  Using built-in camera as fallback")
                    src = 0
                else:
                    logging.error("❌ Fallback camera also failed")
                    logging.error("💡 Try running --list-cameras to see available options")
                    return 1
            else:
                logging.error("💡 Suggestions:")
                logging.error("   • Run --list-cameras to see available cameras")
                logging.error("   • Check camera permissions in System Preferences")
                logging.error("   • Try different camera index: --source 1, --source 2")
                logging.error("   • Ensure no other app is using the camera")
                return 1
            
        # Test camera by reading a frame
        ret, test_frame = cap.read()
        if not ret:
            logging.error(f"❌ Camera {src} opened but cannot read frames")
            logging.error("💡 Try a different camera or check camera connection")
            return 1
            
        logging.info(f"✅ Camera {src} opened successfully ({test_frame.shape[1]}x{test_frame.shape[0]})")
        
        consecutive_failures = 0
        max_failures = 5
        
        while True:
            ret, frame = cap.read()
            if not ret:
                consecutive_failures += 1
                if consecutive_failures >= max_failures:
                    logging.error(f"❌ Camera failed to read {max_failures} consecutive frames")
                    logging.error("💡 Camera may have disconnected or been claimed by another app")
                    break
                logging.warning(f"⚠️  Failed to read frame ({consecutive_failures}/{max_failures}), retrying...")
                time.sleep(0.1)
                continue
            
            # Reset failure counter on successful read
            consecutive_failures = 0
                
            frame_count += 1
            
            # YOLO classification (automatic preprocessing)
            results = model(frame, verbose=False)
            r = results[0]  # Single result for classification
            
            # Process classification result through scare controller
            result = controller.process_classification(r)
            
            # Show video with classification results
            if args.show:
                display_frame = frame.copy()
                
                # Add status overlay
                status_color = (0, 255, 0) if result['state'] == "idle" else (0, 0, 255)
                cv2.putText(display_frame, f"State: {result['state'].upper()}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
                cv2.putText(display_frame, f"Frame: {frame_count}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(display_frame, f"Class: {result['class_name']}", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(display_frame, f"Confidence: {result['confidence']:.1%}", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Add threshold indicator
                threshold_color = (0, 255, 0) if result['confidence'] >= controller.confidence_threshold else (0, 0, 255)
                cv2.putText(display_frame, f"Threshold: {controller.confidence_threshold:.0%}", (10, 190), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, threshold_color, 2)
                
                cv2.imshow("YOLO Hand Classification → VPT8", display_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == ord('q'):  # ESC or Q
                    logging.info("User requested exit")
                    break
            
            # Debug info every 100 frames
            if args.debug and frame_count % 100 == 0:
                logging.debug(f"Frame {frame_count}, State: {result['state']}, Class: {result['class_name']}, Conf: {result['confidence']:.1%}")
                
        cap.release()
                
    except KeyboardInterrupt:
        logging.info("Interrupted by user (Ctrl+C)")
    except Exception as e:
        logging.error(f"Error during processing: {e}")
        return 1
    finally:
        # Return to idle state
        logging.info("Returning to IDLE state...")
        controller.set_mix_fader(0.0)
        
        if args.show:
            cv2.destroyAllWindows()
        logging.info("Cleanup complete")
    
    logging.info("Hand detection bridge stopped")
    return 0

if __name__ == "__main__":
    main()