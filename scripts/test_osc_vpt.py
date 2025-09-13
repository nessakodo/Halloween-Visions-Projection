#!/usr/bin/env python3
"""
Test OSC Row 8 Mix Fader Control
- Load idle video in one input to row 8
- Load scare video in another input to row 8
- Control the mix fader on row 8 to blend between them
- Route row 8 to projection layer
"""

import time
import threading
from pythonosc.udp_client import SimpleUDPClient

HOST, PORT = "127.0.0.1", 6666
client = SimpleUDPClient(HOST, PORT)
lock = threading.Lock()

def control_mix_fader(mix_value, delay=0.5):
    """
    Control row 8 mix fader
    mix_value: 0.0 to 1.0 (0.0 = first input, 1.0 = second input)
    """
    with lock:
        print(f"Setting row 8 mix fader to {mix_value}")
        # Try different possible OSC paths for row 8 mix
        client.send_message("/sources/8video/mixfader", float(mix_value))
        client.send_message("/sources/8video/mix", float(mix_value))
        client.send_message("/sources/8/mixfader", float(mix_value))
        client.send_message("/sources/8/mix", float(mix_value))
        client.send_message("/8video/mixfader", float(mix_value))
        client.send_message("/8video/mix", float(mix_value))
        time.sleep(delay)

def main():
    print("Testing OSC Row 8 Mix Fader Control...")
    print("Setup required:")
    print("1. Route idle video to one input of row 8 mixer")
    print("2. Route scare video to another input of row 8 mixer") 
    print("3. Route row 8 output to your projection layer")
    print("4. OSC enabled on port 6666")
    print("5. Watch the mix fader on row 8 move")
    print()
    
    try:
        print("✓ OSC client created")
        print("Testing row 8 mix fader control...")
        print("(Trying multiple OSC path variations)")
        print()
        
        print("1. Full first input (mix = 0.0)")
        control_mix_fader(0.0, delay=3.0)
        
        print("2. Full second input (mix = 1.0)")
        control_mix_fader(1.0, delay=3.0)
        
        print("3. 50/50 mix (mix = 0.5)")
        control_mix_fader(0.5, delay=3.0)
        
        print("4. Back to first input (mix = 0.0)")
        control_mix_fader(0.0, delay=3.0)
        
        print("5. Smooth crossfade animation")
        for i in range(21):
            mix_val = i / 20.0  # 0.0 to 1.0 in 21 steps
            print(f"   Mix = {mix_val:.2f}")
            control_mix_fader(mix_val, delay=0.2)
        
        print("6. Quick scare effects")
        for _ in range(3):
            control_mix_fader(1.0, delay=0.1)  # Flash to scare
            control_mix_fader(0.0, delay=0.5)  # Back to idle
        
        print("\n✓ Row 8 mix fader test completed!")
        print("Check VPT8 to see if the row 8 mix fader moved.")
        print("If the fader moved but no visual change, check your routing.")
        
    except Exception as e:
        print(f"✗ OSC test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())