#!/usr/bin/env python3
"""
YOLO Hand Detection → VLC Video Projection System
- Real-time hand detection using YOLO
- Direct video playback on projector using python-vlc
- Simple setup without mapping software
- Fullscreen projection with state-based video switching
"""

import argparse
import time
import logging
import threading
import platform
import os
from ultralytics import YOLO
import cv2
import vlc

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
                print(f"  python scripts/yolo_vlc_projection.py --show")
            else:
                print(f"  # Use external camera {cam['index']}")
                print(f"  python scripts/yolo_vlc_projection.py --source {cam['index']} --show")
    
    return available_cameras

def detect_displays():
    """Detect available displays for projector setup"""
    displays = []
    
    if platform.system() == "Darwin":  # macOS
        try:
            import subprocess
            result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], 
                                  capture_output=True, text=True)
            output = result.stdout
            
            # Simple parsing - count displays mentioned
            display_count = output.count('Display Type:')
            for i in range(display_count):
                displays.append(f"Display {i}")
                
        except Exception as e:
            logging.warning(f"Could not detect displays on macOS: {e}")
            displays = ["Main Display", "Secondary Display (if connected)"]
    
    elif platform.system() == "Windows":
        try:
            import win32api
            monitors = win32api.EnumDisplayMonitors()
            for i, monitor in enumerate(monitors):
                displays.append(f"Display {i+1}")
        except Exception as e:
            logging.warning(f"Could not detect displays on Windows: {e}")
            displays = ["Primary Display", "Secondary Display (if connected)"]
    
    else:  # Linux
        displays = ["Display 0", "Display 1 (if connected)"]
    
    return displays

class VLCProjectionController:
    def __init__(self, video_sleep_path="videos/sleeping_face.mp4", 
                 video_scare_path="videos/angry_face.mp4", 
                 fullscreen_display=None):
        """
        Initialize VLC player for projection
        
        Args:
            video_sleep_path: Path to idle/sleeping video
            video_scare_path: Path to scare/alert video  
            fullscreen_display: Display index for fullscreen (None = primary)
        """
        self.video_sleep_path = video_sleep_path
        self.video_scare_path = video_scare_path
        self.fullscreen_display = fullscreen_display
        
        # VLC setup
        vlc_args = [
            '--intf', 'dummy',  # No interface
            '--no-audio',       # Disable audio for now
            '--video-on-top',   # Keep video on top
            '--no-video-title-show',  # Don't show filename
        ]
        
        # Add fullscreen display option if specified
        if fullscreen_display is not None:
            vlc_args.extend(['--fullscreen', '--monitor', str(fullscreen_display)])
        
        self.instance = vlc.Instance(vlc_args)
        self.player = self.instance.media_player_new()
        
        # State management
        self.lock = threading.Lock()
        self.state = "idle"  # "idle" or "scare"
        self.confidence_threshold = 0.99  # 99% confidence required
        self.scare_duration = 2.0  # seconds to stay in scare mode
        self.last_trigger = 0.0
        self.debounce_time = 0.5  # Minimum time between state changes
        self.last_state_change = 0.0
        
        # Verify video files exist
        self._verify_video_files()
        
        logging.info(f"VLCProjectionController initialized")
        logging.info(f"Sleep video: {self.video_sleep_path}")
        logging.info(f"Scare video: {self.video_scare_path}")
        logging.info(f"Confidence threshold: {self.confidence_threshold:.0%}")
        logging.info(f"Scare duration: {self.scare_duration}s")
        if fullscreen_display is not None:
            logging.info(f"Fullscreen display: {fullscreen_display}")
    
    def _verify_video_files(self):
        """Check that video files exist"""
        for video_path in [self.video_sleep_path, self.video_scare_path]:
            if not os.path.exists(video_path):
                logging.warning(f"⚠️  Video file not found: {video_path}")
                logging.warning("💡 Create videos/ directory and add sleeping_face.mp4 and angry_face.mp4")
    
    def cleanup(self):
        """Clean up VLC resources"""
        if self.player:
            self.player.stop()
            self.player.release()
        if self.instance:
            self.instance.release()
        logging.info("VLC resources cleaned up")
    
    def play_video(self, video_path, loop=True):
        """Play video using VLC app directly"""
        with self.lock:
            if not os.path.exists(video_path):
                logging.error(f"❌ Video file not found: {video_path}")
                return False
            
            try:
                # Close any existing VLC
                import subprocess
                subprocess.run(['pkill', 'VLC'], capture_output=True)
                time.sleep(0.2)
                
                # Launch VLC using macOS open command
                abs_path = os.path.abspath(video_path)
                cmd = ['open', '-a', 'VLC', abs_path]
                
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logging.info(f"🎬 Playing: {os.path.basename(video_path)}")
                return True
                
            except Exception as e:
                logging.error(f"❌ Failed to play video {video_path}: {e}")
                return False
    
    def set_state(self, new_state):
        """Switch video based on state: 'idle' or 'scare'"""
        now = time.time()
        
        # Debounce: prevent rapid state changes
        if (now - self.last_state_change) < self.debounce_time:
            return
        
        if new_state == "idle" and self.state != "idle":
            logging.info("   → Switching to IDLE state (sleep video)")
            self.play_video(self.video_sleep_path)
            self.state = "idle"
            self.last_state_change = now
            
        elif new_state == "scare" and self.state != "scare":
            logging.info("   → Switching to SCARE state (scare video)")
            self.play_video(self.video_scare_path)
            self.state = "scare"
            self.last_trigger = now
            self.last_state_change = now
    
    def process_classification(self, result):
        """Process YOLO classification result and trigger video switch if hand detected"""
        now = time.time()
        
        # Get classification results
        confidence = result.probs.top1conf.item()  # 0.0 to 1.0
        class_name = result.names[result.probs.top1]  # 'hand' or 'not_hand'
        
        # State machine logic
        if class_name == 'hand' and confidence >= self.confidence_threshold and self.state != "scare":
            logging.info(f"🖐️  HAND DETECTED! Confidence: {confidence:.1%}")
            self.set_state("scare")
            
        elif self.state == "scare" and (now - self.last_trigger) >= self.scare_duration:
            logging.info("   → SCARE timeout, returning to IDLE")
            self.set_state("idle")
        
        return {
            'confidence': confidence,
            'class_name': class_name,
            'state': self.state
        }

def parse_args():
    p = argparse.ArgumentParser(description="YOLO Hand Detection → VLC Video Projection")
    p.add_argument("--model", default="Colin1.pt", help="YOLO model file (hand detection)")
    p.add_argument("--source", default=0, help="Camera index (0=built-in, 1=external, etc.) or video file")
    p.add_argument("--list-cameras", action="store_true", help="List available cameras and exit")
    p.add_argument("--list-displays", action="store_true", help="List available displays and exit")
    p.add_argument("--conf", type=float, default=0.5, help="YOLO detection confidence")
    p.add_argument("--scare-conf", type=float, default=0.99, help="Confidence threshold for scare trigger")
    p.add_argument("--scare-duration", type=float, default=2.0, help="Scare duration in seconds")
    p.add_argument("--video-sleep", default="videos/sleeping_face.mp4", help="Path to sleep/idle video")
    p.add_argument("--video-scare", default="videos/angry_face.mp4", help="Path to scare/alert video")
    p.add_argument("--fullscreen-display", type=int, help="Display index for fullscreen projection")
    p.add_argument("--show", action="store_true", help="Show camera window with detections")
    p.add_argument("--debug", action="store_true", help="Enable debug logging")
    return p.parse_args()

def main():
    args = parse_args()
    
    # Handle camera listing
    if args.list_cameras:
        list_available_cameras()
        return 0
    
    # Handle display listing
    if args.list_displays:
        print("🖥️  Available displays:")
        displays = detect_displays()
        for i, display in enumerate(displays):
            print(f"  {i}: {display}")
        print(f"\nUsage: --fullscreen-display 1 (for secondary display)")
        return 0
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logging.info("=" * 60)
    logging.info("YOLO Hand Detection → VLC Video Projection")
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
    
    # Initialize VLC projection controller
    controller = VLCProjectionController(
        video_sleep_path=args.video_sleep,
        video_scare_path=args.video_scare,
        fullscreen_display=args.fullscreen_display
    )
    controller.confidence_threshold = args.scare_conf
    controller.scare_duration = args.scare_duration
    
    # Start in idle state (sleep video)
    logging.info("Starting in IDLE state...")
    controller.set_state("idle")
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
        cap = cv2.VideoCapture(src)
        
        if not cap.isOpened():
            logging.error(f"❌ Could not open camera/video source: {src}")
            
            # Try fallback cameras if using camera index
            if isinstance(src, int) and src != 0:
                logging.info("🔄 Attempting fallback to built-in camera (index 0)...")
                cap = cv2.VideoCapture(0)
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
            
        # Test camera by reading a frame (with USB camera initialization delay)
        if isinstance(src, int) and src > 0:
            logging.info("⏳ Initializing USB camera...")
            time.sleep(2)  # Give USB cameras time to initialize
        
        ret, test_frame = cap.read()
        if not ret:
            # Try a few more times for USB cameras
            for attempt in range(3):
                logging.info(f"🔄 Camera initialization attempt {attempt + 2}...")
                time.sleep(1)
                ret, test_frame = cap.read()
                if ret:
                    break
            else:
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
            
            # Process classification result through projection controller
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
                
                cv2.imshow("YOLO Hand Detection → VLC Projection", display_frame)
                
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
        controller.set_state("idle")
        
        # Clean up resources
        controller.cleanup()
        
        if args.show:
            cv2.destroyAllWindows()
        logging.info("Cleanup complete")
    
    logging.info("VLC projection system stopped")
    return 0

if __name__ == "__main__":
    main()