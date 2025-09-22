#!/usr/bin/env python3
"""
Simple Halloween Hand Detection Projection
- Direct OpenCV window display (no VLC needed)
- Toggle between debug mode and fullscreen projection
- Mirror display setup friendly
"""

import argparse
import time
import logging
import cv2
import numpy as np
from ultralytics import YOLO

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

class SimpleProjectionController:
    def __init__(self, video_sleep_path, video_scare_path):
        self.video_sleep_path = video_sleep_path
        self.video_scare_path = video_scare_path
        self.state = "idle"
        self.confidence_threshold = 0.7
        self.scare_duration = 2.0
        self.last_trigger = 0.0
        self.debug_mode = True
        self.production_mode = False
        
        # Load videos
        self.sleep_cap = cv2.VideoCapture(video_sleep_path)
        self.scare_cap = cv2.VideoCapture(video_scare_path)
        
        if not self.sleep_cap.isOpened():
            raise Exception(f"Could not open sleep video: {video_sleep_path}")
        if not self.scare_cap.isOpened():
            raise Exception(f"Could not open scare video: {video_scare_path}")
        
        # Get video properties
        self.sleep_fps = self.sleep_cap.get(cv2.CAP_PROP_FPS)
        self.scare_fps = self.scare_cap.get(cv2.CAP_PROP_FPS)
        
        self.sleep_frame_count = 0
        self.scare_frame_count = 0
        
        logging.info(f"✅ Videos loaded successfully")
        logging.info(f"Sleep video: {video_sleep_path} ({self.sleep_fps:.1f} FPS)")
        logging.info(f"Scare video: {video_scare_path} ({self.scare_fps:.1f} FPS)")
        
    def get_current_video_frame(self):
        """Get the current frame based on state"""
        if self.state == "scare":
            ret, frame = self.scare_cap.read()
            if not ret:  # Loop back to beginning
                self.scare_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.scare_cap.read()
            return frame
        else:
            ret, frame = self.sleep_cap.read()
            if not ret:  # Loop back to beginning
                self.sleep_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.sleep_cap.read()
            return frame
    
    def process_hand_detection(self, class_name, confidence):
        """Process hand detection and update state"""
        current_time = time.time()
        
        if class_name == 'hand' and confidence >= self.confidence_threshold:
            if self.state != "scare":
                logging.info(f"🖐️  HAND DETECTED! Confidence: {confidence:.1%}")
                logging.info("   → Switching to SCARE state")
                self.state = "scare"
                self.last_trigger = current_time
        
        # Check for scare timeout
        if self.state == "scare" and current_time - self.last_trigger > self.scare_duration:
            logging.info("   → SCARE timeout, returning to IDLE")
            self.state = "idle"
    
    def toggle_debug_mode(self):
        """Toggle between debug and projection modes"""
        self.debug_mode = not self.debug_mode
        mode = "DEBUG" if self.debug_mode else "PROJECTION"
        logging.info(f"🔄 Switched to {mode} mode")
        return self.debug_mode
    
    def toggle_production_mode(self):
        """Toggle production mode for different aspect ratios"""
        self.production_mode = not self.production_mode
        mode = "PRODUCTION" if self.production_mode else "NORMAL"
        logging.info(f"🔄 Switched to {mode} display mode")
        return self.production_mode
    
    def create_debug_display(self, camera_frame, video_frame, class_name, confidence, model_name="Colin1.pt"):
        """Create debug display with camera feed and info overlay"""
        # Resize camera frame for corner display
        cam_h, cam_w = camera_frame.shape[:2]
        scale = 0.3
        small_cam = cv2.resize(camera_frame, (int(cam_w * scale), int(cam_h * scale)))
        
        # Use video frame as background - ensure it's the right size
        display_h, display_w = camera_frame.shape[:2]  # Use camera resolution
        display = cv2.resize(video_frame, (display_w, display_h))
        
        # Overlay camera feed in top-right corner
        cam_h_small, cam_w_small = small_cam.shape[:2]
        display_h, display_w = display.shape[:2]
        
        # Position in top-right corner
        y_offset = 20
        x_offset = display_w - cam_w_small - 20
        
        # Create border around camera feed
        cv2.rectangle(display, 
                     (x_offset - 5, y_offset - 5), 
                     (x_offset + cam_w_small + 5, y_offset + cam_h_small + 5), 
                     (255, 255, 255), 2)
        
        # Overlay camera feed
        display[y_offset:y_offset + cam_h_small, x_offset:x_offset + cam_w_small] = small_cam
        
        # Add debug information
        info_y = 50
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        
        # State info
        state_color = (0, 0, 255) if self.state == "scare" else (0, 255, 0)
        cv2.putText(display, f"State: {self.state.upper()}", (20, info_y), 
                   font, font_scale, state_color, thickness)
        
        # Detection info
        detection_color = (0, 255, 255) if class_name == 'hand' else (255, 255, 255)
        cv2.putText(display, f"Detection: {class_name} ({confidence:.1%})", 
                   (20, info_y + 50), font, font_scale, detection_color, thickness)
        
        # Threshold info
        cv2.putText(display, f"Threshold: {self.confidence_threshold:.0%}", 
                   (20, info_y + 100), font, font_scale, (255, 255, 255), thickness)
        
        # Model info
        cv2.putText(display, f"Model: {model_name}", 
                   (20, info_y + 150), font, font_scale, (255, 255, 255), thickness)
        
        # Instructions
        cv2.putText(display, "Press 'D' to toggle debug/projection mode", 
                   (20, display_h - 120), font, 0.7, (255, 255, 255), 2)
        cv2.putText(display, "Press 'P' for production mode (grey fix)", 
                   (20, display_h - 90), font, 0.7, (255, 255, 255), 2)
        cv2.putText(display, "Press 'F' for fullscreen", 
                   (20, display_h - 60), font, 0.7, (255, 255, 255), 2)
        cv2.putText(display, "Press 'Q' or ESC to quit", 
                   (20, display_h - 30), font, 0.7, (255, 255, 255), 2)
        
        return display
    
    
    def create_production_display(self, video_frame):
        """Create production display with different sizing to minimize grey border"""
        h, w = video_frame.shape[:2]
        
        # Try stretching the video slightly taller to fill potential grey space
        stretched_h = int(h * 1.1)
        production_frame = cv2.resize(video_frame, (w, stretched_h))
        
        # Crop back to original height from the middle
        crop_start = (stretched_h - h) // 2
        production_frame = production_frame[crop_start:crop_start + h, :]
        
        return production_frame
    

def main():
    parser = argparse.ArgumentParser(description="Simple Halloween Hand Detection Projection")
    parser.add_argument("--model", default="Colin1.pt", help="YOLO model file")
    parser.add_argument("--source", default=0, help="Camera index")
    parser.add_argument("--video-sleep", default="videos/sleeping_face.mp4", help="Sleep video")
    parser.add_argument("--video-scare", default="videos/angry_face.mp4", help="Scare video")
    parser.add_argument("--conf", type=float, default=0.7, help="Hand detection confidence threshold")
    parser.add_argument("--fullscreen", action="store_true", help="Start in fullscreen mode")
    
    args = parser.parse_args()
    
    logging.info("=" * 60)
    logging.info("🎃 Simple Halloween Hand Detection Projection")
    logging.info("=" * 60)
    
    # Load YOLO model
    try:
        logging.info(f"Loading YOLO model: {args.model}")
        model = YOLO(args.model)
        logging.info(f"✓ Model loaded: {model.names}")
    except Exception as e:
        logging.error(f"Failed to load YOLO model: {e}")
        return 1
    
    # Initialize projection controller
    try:
        controller = SimpleProjectionController(args.video_sleep, args.video_scare)
        controller.confidence_threshold = args.conf
    except Exception as e:
        logging.error(f"Failed to initialize controller: {e}")
        return 1
    
    # Set up camera
    try:
        source = int(args.source)
    except ValueError:
        source = args.source
    
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        logging.error(f"Could not open camera: {source}")
        return 1
    
    logging.info(f"✅ Camera opened: {args.source}")
    logging.info(f"Confidence threshold: {args.conf:.0%}")
    logging.info("🎮 Controls:")
    logging.info("  D = Toggle Debug/Projection mode")
    logging.info("  P = Toggle Production mode (grey border fix)")
    logging.info("  F = Toggle fullscreen")
    logging.info("  Q/ESC = Quit")
    logging.info("-" * 60)
    
    # Create display window
    window_name = "Halloween Projection"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    if args.fullscreen:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    try:
        while True:
            # Read camera frame
            ret, camera_frame = cap.read()
            if not ret:
                logging.warning("Failed to read camera frame")
                continue
            
            # Get current video frame
            video_frame = controller.get_current_video_frame()
            if video_frame is None:
                continue
            
            # Resize video frame to exactly match camera resolution, adding extra height to eliminate grey
            cam_h, cam_w = camera_frame.shape[:2]
            # Add 15% extra height to ensure no grey top border
            extended_h = int(cam_h * 1.15)
            video_frame = cv2.resize(video_frame, (cam_w, extended_h))
            
            # Crop from bottom to keep original height but eliminate grey at top
            video_frame = video_frame[:cam_h, :]
            
            # Run YOLO classification on camera frame
            results = model.predict(camera_frame, verbose=False)
            
            class_name = "not_hand"
            confidence = 0.0
            
            if results and len(results) > 0:
                result = results[0]
                # Handle classification results (not detection)
                if hasattr(result, 'probs') and result.probs is not None:
                    # Classification model - get class probabilities
                    probs = result.probs.data.cpu().numpy()
                    max_idx = probs.argmax()
                    confidence = probs[max_idx]
                    class_name = model.names[int(max_idx)]
                else:
                    # Fallback: try to get from names/classes if available
                    try:
                        # Sometimes classification results are in different format
                        class_name = "not_hand"
                        confidence = 0.5
                    except:
                        pass
                
                # Debug: print classification every 30 frames
                if not hasattr(controller, 'frame_count'):
                    controller.frame_count = 0
                controller.frame_count += 1
                if controller.frame_count % 30 == 0:
                    logging.info(f"🔍 Classification: {class_name} ({confidence:.1%})")
            
            # Process detection
            controller.process_hand_detection(class_name, confidence)
            
            # Create display based on mode
            if controller.debug_mode:
                display_frame = controller.create_debug_display(camera_frame, video_frame, class_name, confidence, args.model)
            elif controller.production_mode:
                display_frame = controller.create_production_display(video_frame)
            else:
                display_frame = video_frame
            
            # Show frame
            cv2.imshow(window_name, display_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q'), ord('Q'), 27]:  # Q or ESC
                break
            elif key in [ord('d'), ord('D')]:  # Toggle debug mode
                controller.toggle_debug_mode()
            elif key in [ord('p'), ord('P')]:  # Toggle production mode
                controller.toggle_production_mode()
            elif key in [ord('f'), ord('F')]:  # Toggle fullscreen
                current_state = cv2.getWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN)
                if current_state == cv2.WINDOW_FULLSCREEN:
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                    logging.info("🔄 Switched to windowed mode")
                else:
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    logging.info("🔄 Switched to fullscreen mode")
    
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    
    finally:
        cap.release()
        controller.sleep_cap.release()
        controller.scare_cap.release()
        cv2.destroyAllWindows()
        logging.info("✅ Cleanup complete")

if __name__ == "__main__":
    main()