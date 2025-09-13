# yolo_vpt_bridge.py
# Enhanced YOLO -> VPT bridge with logging and debugging
# pip install ultralytics opencv-python python-osc

import argparse, time
import logging
from datetime import datetime
from ultralytics import YOLO
from pythonosc.udp_client import SimpleUDPClient
import cv2

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--source", default=0, help="camera index or video file")
    p.add_argument("--class-names", nargs="*", default=None)
    p.add_argument("--conf", type=float, default=0.6)
    p.add_argument("--cooldown", type=float, default=1.5)
    p.add_argument("--vpt-host", default="127.0.0.1")
    p.add_argument("--vpt-port", type=int, default=6666)
    p.add_argument("--mode", choices=["clips","presets"], default="clips")
    p.add_argument("--idle-clip", type=int, default=1)
    p.add_argument("--scare-clip", type=int, default=2)
    p.add_argument("--idle-preset", type=int, default=1)
    p.add_argument("--scare-preset", type=int, default=2)
    p.add_argument("--show", action="store_true")
    p.add_argument("--debug", action="store_true", help="Enable debug logging")
    return p.parse_args()

def set_idle(osc, args):
    if args.mode == "clips":
        logging.info(f"→ VPT: Switching to idle clip {args.idle_clip}")
        osc.send_message("/sources/1video/clipnr", args.idle_clip)
        osc.send_message("/sources/1video/start", [])
    else:
        logging.info(f"→ VPT: Switching to idle preset {args.idle_preset}")
        osc.send_message("/preset", args.idle_preset)

def set_scare(osc, args):
    if args.mode == "clips":
        logging.info(f"→ VPT: Switching to scare clip {args.scare_clip}")
        osc.send_message("/sources/1video/clipnr", args.scare_clip)
        osc.send_message("/sources/1video/start", [])
    else:
        logging.info(f"→ VPT: Switching to scare preset {args.scare_preset}")
        osc.send_message("/preset", args.scare_preset)

def main():
    args = parse_args()
    
    # Set debug logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled")
    
    logging.info("=" * 50)
    logging.info("Halloween Projection Mapping - YOLO ↔ VPT Bridge")
    logging.info("=" * 50)
    
    # Load YOLO model (using YOLO11 best practices)
    try:
        logging.info(f"Loading YOLO model: {args.model}")
        model = YOLO(args.model)
        logging.info(f"✓ Model loaded: {model.model_name if hasattr(model, 'model_name') else 'YOLO'}")
        logging.info(f"✓ Classes available: {len(model.names)}")
        if args.debug:
            logging.debug(f"Available classes: {list(model.names.values())[:10]}...")
    except Exception as e:
        logging.error(f"Failed to load YOLO model: {e}")
        logging.error("Tip: Use 'yolov8n.pt' or 'yolo11n.pt' for nano model")
        return 1
    
    # Create OSC client
    try:
        logging.info(f"Connecting to VPT at {args.vpt_host}:{args.vpt_port}")
        osc = SimpleUDPClient(args.vpt_host, args.vpt_port)
        logging.info("✓ OSC client created")
    except Exception as e:
        logging.error(f"Failed to create OSC client: {e}")
        return 1
    
    # Configuration summary
    logging.info(f"Mode: {args.mode}")
    if args.mode == "clips":
        logging.info(f"Clips: idle={args.idle_clip}, scare={args.scare_clip}")
    else:
        logging.info(f"Presets: idle={args.idle_preset}, scare={args.scare_preset}")
    
    if args.class_names:
        logging.info(f"Filtering for classes: {args.class_names}")
    else:
        logging.info("Detecting any class")
    
    logging.info(f"Confidence threshold: {args.conf}")
    logging.info(f"Cooldown: {args.cooldown}s")
    
    # Start in idle state
    state = "idle"
    logging.info("Starting in IDLE state")
    set_idle(osc, args)
    last_trigger = 0.0
    frame_count = 0
    
    # Set up video source (using 2024-2025 best practices)
    src = int(args.source) if str(args.source).isdigit() else args.source
    logging.info(f"Opening source: {src}")
    
    # Use YOLO's built-in streaming capabilities (YOLO11 best practice)
    logging.info("✓ Using YOLO built-in streaming for optimal performance")
    logging.info("Press ESC to quit (when --show is enabled), or Ctrl+C to stop")
    logging.info("-" * 50)
    
    try:
        # Use YOLO11's optimized streaming prediction (memory-efficient generator)
        results = model.predict(
            source=src, 
            stream=True,          # Memory-efficient streaming
            conf=args.conf,
            imgsz=640,
            verbose=False,
            show=False,           # We handle display manually
            save=False            # Don't save results
        )
        
        for r in results:
            frame_count += 1
            detected = False
            detected_objects = []
            
            # Process detections using YOLO11 best practices
            if r.boxes is not None:
                boxes = r.boxes
                for i in range(len(boxes)):
                    # Get detection info
                    cls_id = int(boxes.cls[i])
                    conf = float(boxes.conf[i])
                    cname = r.names.get(cls_id, f"class_{cls_id}")
                    
                    detected_objects.append({
                        'class': cname,
                        'confidence': conf,
                        'bbox': boxes.xyxy[i].tolist() if hasattr(boxes, 'xyxy') else None
                    })
                    
                    # Check if this detection matches our target classes
                    if args.class_names is None or cname in args.class_names:
                        detected = True
                        
                        if args.debug:
                            logging.debug(f"Target detected: {cname} ({conf:.2f})")
            
            # Show video with detections (YOLO11 optimized display)
            if args.show:
                # Use YOLO's built-in plot method for optimized display
                annotated_frame = r.plot()
                
                # Add custom status overlay
                status_color = (0, 255, 0) if state == "idle" else (0, 0, 255)
                cv2.putText(annotated_frame, f"State: {state.upper()}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
                cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Add detection count
                if detected_objects:
                    cv2.putText(annotated_frame, f"Objects: {len(detected_objects)}", (10, 110), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow("YOLO11 -> VPT Bridge", annotated_frame)
                
                # Check for ESC key press
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    logging.info("User requested exit (ESC pressed)")
                    break
                elif key == ord('q'):  # Q key (YOLO11 standard)
                    logging.info("User requested exit (Q pressed)")
                    break
            
            # State machine logic
            now = time.time()
            time_since_last = now - last_trigger
            
            if detected and state != "scare" and time_since_last > args.cooldown:
                logging.info(f"🎯 DETECTION! Objects: {[obj['class'] for obj in detected_objects if args.class_names is None or obj['class'] in args.class_names]}")
                set_scare(osc, args)
                state = "scare"
                last_trigger = now
                
            elif not detected and state != "idle" and time_since_last > args.cooldown:
                logging.info("😴 No detection, returning to idle")
                set_idle(osc, args)
                state = "idle"
                last_trigger = now
            
            # Debug info every 100 frames
            if args.debug and frame_count % 100 == 0:
                logging.debug(f"Frame {frame_count}, State: {state}, Objects: {len(detected_objects)}")
                
    except KeyboardInterrupt:
        logging.info("Interrupted by user (Ctrl+C)")
    except Exception as e:
        logging.error(f"Error during processing: {e}")
        return 1
    finally:
        # YOLO11 handles cleanup automatically, but ensure CV2 windows are closed
        if args.show:
            cv2.destroyAllWindows()
        logging.info("Cleanup complete")
    
    logging.info("Bridge stopped")
    return 0

if __name__ == "__main__":
    main()
