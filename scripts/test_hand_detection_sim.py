#!/usr/bin/env python3
"""
Simulate Hand Detection for VPT8 Scare System
- Simulates YOLO hand detection at various confidence levels
- Triggers scare effect when confidence >= 90%
- Tests the logic before integrating real YOLO
"""

import time
import random
import threading
from pythonosc.udp_client import SimpleUDPClient

HOST, PORT = "127.0.0.1", 6666
client = SimpleUDPClient(HOST, PORT)
lock = threading.Lock()

class ScareController:
    def __init__(self):
        self.state = "idle"  # "idle" or "scare"
        self.confidence_threshold = 0.90
        self.scare_duration = 2.0  # seconds to stay in scare mode
        self.last_trigger = 0.0
        
    def set_mix_fader(self, value):
        """Control the row 8 mix fader (0.0=idle, 1.0=scare)"""
        with lock:
            print(f"   → Setting mix fader to {value}")
            # Use all the working OSC paths from successful test
            client.send_message("/sources/8video/mixfader", float(value))
            client.send_message("/sources/8video/mix", float(value))
            client.send_message("/sources/8/mixfader", float(value))
            client.send_message("/sources/8/mix", float(value))
            client.send_message("/8video/mixfader", float(value))
            client.send_message("/8video/mix", float(value))
    
    def trigger_scare(self, confidence):
        """Trigger scare effect if confidence is high enough"""
        now = time.time()
        
        if confidence >= self.confidence_threshold and self.state != "scare":
            print(f"🖐️  HAND DETECTED! Confidence: {confidence:.1%}")
            print("   → Triggering SCARE mode")
            self.set_mix_fader(1.0)  # Switch to scare video
            self.state = "scare"
            self.last_trigger = now
            return True
            
        elif self.state == "scare" and (now - self.last_trigger) >= self.scare_duration:
            print("   → Returning to IDLE mode")
            self.set_mix_fader(0.0)  # Switch back to idle
            self.state = "idle"
            return True
            
        return False

def simulate_detection_cycle(controller):
    """Simulate a realistic detection scenario"""
    print("\n--- Simulating Hand Detection Cycle ---")
    
    scenarios = [
        (0.15, "Low confidence - person in background"),
        (0.45, "Medium confidence - partial hand visible"),
        (0.73, "High confidence - hand visible but not clear"),
        (0.92, "TRIGGER! Clear hand detection"),
        (0.94, "TRIGGER! Hand still visible"),
        (0.88, "Just below threshold - hand moving away"),
        (0.23, "Low confidence - hand gone"),
        (0.05, "Very low - no hand"),
        (0.0, "No detection"),
    ]
    
    for confidence, description in scenarios:
        print(f"\nSimulated confidence: {confidence:.1%} - {description}")
        
        triggered = controller.trigger_scare(confidence)
        if triggered:
            print(f"   State changed to: {controller.state}")
        else:
            print(f"   State remains: {controller.state}")
            
        time.sleep(1.5)  # Simulate frame processing time
        
        # Check for automatic return to idle
        controller.trigger_scare(0.0)  # Force state check

def interactive_test(controller):
    """Interactive testing mode"""
    print("\n--- Interactive Mode ---")
    print("Enter confidence values (0.0-1.0) or 'q' to quit:")
    print("Try values like: 0.5, 0.85, 0.92, 0.95")
    
    while True:
        try:
            user_input = input(f"\nCurrent state: {controller.state} | Enter confidence: ")
            
            if user_input.lower() == 'q':
                break
                
            confidence = float(user_input)
            if 0.0 <= confidence <= 1.0:
                triggered = controller.trigger_scare(confidence)
                if triggered:
                    print(f"   → State: {controller.state}")
                    
                # Auto-return to idle after duration
                time.sleep(0.1)
                controller.trigger_scare(0.0)
            else:
                print("Please enter a value between 0.0 and 1.0")
                
        except ValueError:
            print("Please enter a valid number or 'q' to quit")
        except KeyboardInterrupt:
            break

def main():
    print("Hand Detection Simulation for VPT8 Scare System")
    print("=" * 50)
    print(f"Confidence threshold: 90%")
    print(f"Scare duration: 2.0 seconds")
    print(f"VPT8 OSC: {HOST}:{PORT}")
    print()
    
    controller = ScareController()
    
    # Start in idle state
    print("Starting in IDLE state...")
    controller.set_mix_fader(0.0)
    time.sleep(1)
    
    try:
        # Run simulation cycle
        simulate_detection_cycle(controller)
        
        # Interactive testing
        interactive_test(controller)
        
    except KeyboardInterrupt:
        print("\nStopping simulation...")
    
    finally:
        # Return to idle state
        print("Returning to IDLE state...")
        controller.set_mix_fader(0.0)
        print("✓ Simulation complete")

if __name__ == "__main__":
    main()