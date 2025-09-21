#!/usr/bin/env python3
"""Manual OSC test script for HeavyM sequence control"""

import time
import argparse
from pythonosc.udp_client import SimpleUDPClient

def main():
    parser = argparse.ArgumentParser(description="Manual HeavyM OSC Test")
    parser.add_argument("--host", default="127.0.0.1", help="HeavyM host")
    parser.add_argument("--port", type=int, default=7000, help="HeavyM OSC port")
    parser.add_argument("--sequence", choices=["sleep", "scare", "both"], default="both", 
                       help="Which sequence to trigger")
    parser.add_argument("--delay", type=float, default=2.0, 
                       help="Delay between sequences (for 'both' mode)")
    args = parser.parse_args()

    client = SimpleUDPClient(args.host, args.port)
    
    print(f"🎯 Sending OSC to HeavyM at {args.host}:{args.port}")
    
    if args.sequence in ["sleep", "both"]:
        print("📤 Sending: /sequences/SleepSeq/select 1.0")
        client.send_message("/sequences/SleepSeq/select", 1.0)
        if args.sequence == "both":
            print(f"⏱️  Waiting {args.delay}s...")
            time.sleep(args.delay)
    
    if args.sequence in ["scare", "both"]:
        print("📤 Sending: /sequences/ScareSeq/select 1.0")
        client.send_message("/sequences/ScareSeq/select", 1.0)
    
    print("✅ Test messages sent!")
    print("\n💡 Expected behavior:")
    print("   - HeavyM should switch sequences immediately")
    print("   - Check HeavyM's sequence panel for active sequence")
    print("   - If nothing happens, verify sequence names in HeavyM")

if __name__ == "__main__":
    main()