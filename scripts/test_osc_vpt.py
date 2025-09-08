#!/usr/bin/env python3
"""
Test OSC communication with VPT
Make sure VPT is running with OSC enabled on port 6666 before running this
"""

import time
from pythonosc.udp_client import SimpleUDPClient

def main():
    print("Testing OSC communication with VPT...")
    print("Make sure VPT is running with OSC enabled on port 6666!")
    print("Watch the VPT OSC monitor to see if messages are received.")
    print()
    
    try:
        # Create OSC client
        client = SimpleUDPClient("127.0.0.1", 6666)
        print("✓ OSC client created")
        
        # Send test messages
        print("\nSending test messages...")
        
        print("1. Switching to clip 1 (idle)")
        client.send_message("/sources/1video/clipnr", 1)
        client.send_message("/sources/1video/start", [])
        time.sleep(2)
        
        print("2. Switching to clip 2 (scare)")
        client.send_message("/sources/1video/clipnr", 2)
        client.send_message("/sources/1video/start", [])
        time.sleep(2)
        
        print("3. Back to clip 1 (idle)")
        client.send_message("/sources/1video/clipnr", 1)
        client.send_message("/sources/1video/start", [])
        
        print("\n✓ Test messages sent successfully!")
        print("Check VPT to see if the clips switched.")
        print("If VPT shows 'Receiving OSC' messages, communication is working!")
        
    except Exception as e:
        print(f"✗ OSC test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())